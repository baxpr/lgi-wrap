#!/usr/bin/env python

import argparse
import nibabel.freesurfer.io
import numpy

from pathlib import Path


parser = argparse.ArgumentParser()
parser.add_argument('--lgi_dir', required=True)
args = parser.parse_args()

# Find {lh,rh}.pial.lgi.map.{kernel}.txt files
lgi_path = Path(args.lgi_dir)
lgi_files = lgi_path.glob('?h.pial.lgi.*.txt'))
lgifile_paths = [str(f) for f in files if f.is_file()]

# Then convert each txt file (keep participant kernel size for now)
for lgifile_path in lgifile_paths:
    vals = numpy.loadtxt(lgifile_path).astype(numpy.float32)
    out_path = lgifile_path.replace('.txt', '.curv')
    nibabel.freesurfer.io.write_morph_data(out_path, vals)

