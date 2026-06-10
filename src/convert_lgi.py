#!/usr/bin/env python

import numpy
import nibabel.freesurfer.io

vals = numpy.loadtxt("10013-01/OUTPUTS/lh.pial.lgi.map.181.txt").astype(numpy.float32)
nibabel.freesurfer.io.write_morph_data("10013-01/OUTPUTS/lh.lgi.curv", vals)
