#!/usr/bin/env bash
#
# Prep for https://github.com/ilwoolyu/LocalGyrificationIndex
#
# Requires a freesurfer container of appropriate version

# Defaults
export fs_dir=/INPUTS/freesurfer/SUBJECT
export out_dir=/OUTPUTS

# Parse input 
while [[ $# -gt 0 ]]; do
    key="${1}"
    case $key in   
        --fs_dir)     export fs_dir="${2}";     shift; shift ;;
        --out_dir)    export out_dir="${2}";    shift; shift ;;
        *) echo "Input ${1} not recognized" ; shift ;;
    esac
done

mkdir -p "${out_dir}"

mris_convert "${fs_dir}"/surf/lh.pial "${out_dir}"/lh.pial.vtk
mris_convert "${fs_dir}"/surf/lh.white "${out_dir}"/lh.white.vtk
mris_convert "${fs_dir}"/surf/rh.pial "${out_dir}"/rh.pial.vtk
mris_convert "${fs_dir}"/surf/rh.white "${out_dir}"/rh.white.vtk
