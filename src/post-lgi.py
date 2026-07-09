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
import pandas
import shutil
import subprocess
from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--lgi_dir', required=True)
parser.add_argument('--subject_dir', required=True)
parser.add_argument('--subjects_dir', required=True)
args = parser.parse_args()

# Reference kernel sizes, hard coded
ref_kernels = [316, 632, 948, 1264]

# Grab freesurfer env and set subjects dir
run_env = os.environ.copy()
run_env["SUBJECTS_DIR"] = args.subjects_dir

# Link fsaverage files to subjects dir
cmd = 'ln -fs $FREESURFER_HOME/subjects/fsaverage $SUBJECTS_DIR/fsaverage'
subprocess.run(cmd, env=run_env, shell=True, check=True)

# lh and rh kernel sizes may differ, need to be tracked separately
for hemi in ['lh', 'rh']:

    # Find {lh,rh}.pial.lgi.map.{kernel}.txt files
    lgi_path = Path(args.lgi_dir)
    lgi_files = list(lgi_path.glob(f'{hemi}.pial.lgi.map.*.txt'))
    lgifile_paths = [str(f) for f in lgi_files if f.is_file()]

    # Then convert each txt file (keep participant kernel size for now)
    for lgifile_path in lgifile_paths:
        vals = numpy.loadtxt(lgifile_path).astype(numpy.float32)
        out_path = lgifile_path.replace('.txt', '.curv')
        nibabel.freesurfer.io.write_morph_data(out_path, vals)

    # Find the newly created {hemi}.pial.lgi.map.{kernel}.curv files
    curv_files = list(lgi_path.glob(f'{hemi}.pial.lgi.map.*.curv'))
    curvfile_paths = [str(f) for f in curv_files if f.is_file()]
    curvfile_names = [f.name for f in curv_files if f.is_file()]

    # Extract the participant kernel sizes and sort
    klist = sorted([int(n.split('.')[4]) for n in curvfile_names])
    if not 'kernels' in locals():
        kernels = pandas.DataFrame({
        'reference_kernel': ref_kernels,
        f'{hemi}_subject_kernel': klist,
        'klist': klist,
        })
    else:
        kernels[f'{hemi}_subject_kernel'] = klist
        kernels['klist'] = klist

    # Make additional outputs for each kernel
    for row in kernels.itertuples():
        print(row)
        
        # Resample LGI surfaces to fsaverage mesh
        cmd = [
            'mri_surf2surf',
            '--srcsubject', f'{args.subject_dir}',
            '--trgsubject', 'fsaverage',
            '--hemi', f'{hemi}',
            '--srcsurfval', f'{args.lgi_dir}/{hemi}.pial.lgi.map.{row.klist}.curv',
            '--src_type', 'curv',
            '--tval', f'{args.lgi_dir}/{hemi}.pial.lgi.fsaverage.{row.reference_kernel:04d}.mgh',
            ]
        subprocess.run(cmd, env=run_env, check=True)

        # Rename files to be friendly for VertexWiseR
        shutil.copy(
            f'{args.lgi_dir}/{hemi}.pial.lgi.map.{row.klist}.curv',
            f'{args.lgi_dir}/{hemi}.pial.lgi.map.ref{row.reference_kernel:04d}',
            )

# Save kernel info
kernels.drop('klist', axis=1, inplace=True)
kernels.to_csv(os.path.join(args.lgi_dir, 'kernel_info.csv'), index=False)
