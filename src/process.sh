#!/usr/bin/env bash

fsdir=$(pwd)/10013-01/freesurfer800_v2
outdir=$(pwd)/10013-01/OUTPUTS

cd "${outdir}"

mris_convert "${fsdir}"/surf/lh.pial lh.pial.vtk
mris_convert "${fsdir}"/surf/lh.white lh.white.vtk

#singularity exec /data/mcr/centos7/singularity/cmorph_1.7.sif \
#    env LANG=C.UTF-8 LC_ALL=C.UTF-8 lgi -i lh.pial.vtk --white lh.white.vtk

singularity exec /data/mcr/centos7/singularity/cmorph_1.7.sif \
env LANG=C.UTF-8 LC_ALL=C.UTF-8 \
lgi -i lh.pial.vtk \
--white lh.white.vtk \
--ref 77100 \
--kernel 1264 \
--intv 316


# To common grid
SUBJECTS_DIR=$(pwd)/10007-01
ln -s "$FREESURFER_HOME/subjects/fsaverage" "$SUBJECTS_DIR/fsaverage"
mri_surf2surf \
    --srcsubject freesurfer800_v2 \
    --trgsubject fsaverage \
    --hemi lh \
    --sval "$SUBJECTS_DIR/OUTPUTS/lh.lgi.curv" \
    --tval "$SUBJECTS_DIR/OUTPUTS/lh.lgi.fsaverage.mgh"
