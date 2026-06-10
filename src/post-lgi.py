#!/usr/bin/env python
#
# NOTE: Default reference space kernel sizes of 316 / 632 / 948 / 1264 are 
# assumed and hard-coded in the output filenames. Corresponding options for 
# the cmorph 1.7 pipeline are
#
#     --ref 77100 --kernel 1264 --intv 316
#
# following
#
# Lyu I, Kim SH, Girault JB, Gilmore JH, Styner MA. A cortical shape-adaptive 
# approach to local gyrification index. Med Image Anal. 2018 Aug;48:244-258. 
# doi: 10.1016/j.media.2018.06.009. PMID: 29990689; PMCID: PMC6167255.

import argparse
import nibabel
import numpy
import os
import subprocess
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--lgi_dir', required=True)
args = parser.parse_args()

# Find {lh,rh}.pial.lgi.map.{kernel}.txt files
lgi_path = Path(args.lgi_dir)
lgi_files = list(lgi_path.glob('?h.pial.lgi.map.*.txt'))
lgifile_paths = [str(f) for f in lgi_files if f.is_file()]

# Then convert each txt file (keep participant kernel size for now)
for lgifile_path in lgifile_paths:
    vals = numpy.loadtxt(lgifile_path).astype(numpy.float32)
    out_path = lgifile_path.replace('.txt', '.curv')
    nibabel.freesurfer.io.write_morph_data(out_path, vals)

# Find the newly created {lh,rh}.pial.lgi.map.{kernel}.curv files
curv_files = list(lgi_path.glob('?h.pial.lgi.map.*.curv'))
curvfile_paths = [str(f) for f in curv_files if f.is_file()]
curvfile_names = [f.name for f in curv_files if f.is_file()]

# Extract the participant kernel sizes and sort
kernels = sorted([int(n.split('.')[4]) for n in curvfile_names])

# Reference kernel sizes
ref_kernels = [316, 632, 948, 1264]

# FIXME
# Let's run mri_surf2surf via subprocess. In our freesurfer container,
# the env should already be in place, we'll only need SUBJECTS_DIR I
# think

# DRAFT below here

def surf2surf(
    subjects_dir,
    srcsubject,
    trgsubject,
    hemi,
    srcval,      # e.g. "thickness" or a path to a .mgh/.mgz
    trgval,      # output file path
    fwhm=None,   # optional smoothing
    env=None,
):
    subjects_dir = str(subjects_dir)
    trgval = str(trgval)

    # Inherit your shell environment where FreeSurfer is already sourced,
    # but ensure SUBJECTS_DIR is set.
    run_env = os.environ.copy()
    if env:
        run_env.update(env)
    run_env["SUBJECTS_DIR"] = subjects_dir

    cmd = [
        "mri_surf2surf",
        "--srcsubject", srcsubject,
        "--trgsubject", trgsubject,
        "--hemi", hemi,
        "--sval", srcval,      # per-vertex data name or file
        "--tval", trgval,
    ]
    if fwhm is not None:
        cmd += ["--fwhm", str(fwhm)]

    subprocess.run(cmd, env=run_env, check=True)
    return Path(trgval)

