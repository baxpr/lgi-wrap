#!/usr/bin/env bash

# Defaults
export lgi_dir=/OUTPUTS

# Parse input 
while [[ $# -gt 0 ]]; do
    key="${1}"
    case $key in   
        --lgi_dir)     export lgi_dir="${2}";     shift; shift ;;
        *) echo "Input ${1} not recognized" ; shift ;;
    esac
done

# Convert surfaces to freesurfer format
convert_lgi.py --lgi_dir "${lgi_dir}"

# FIXME
# Parse filenames to get original and ref space kernel sizes

# Resample to fsaverage grid, correctly renaming to ref space kernel size


