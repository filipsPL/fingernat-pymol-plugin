#!/bin/bash

source activate base

declare -a versions=(pymol-2-0-7 pymol-2-1-1 pymol-2-2-3 pymol-2-3-2 pymol-2-4-0 pymol-2-5-0 pymol-2-5-0-py3)

for version in "${versions[@]}"
do
    echo "$version"

    conda activate $version
    pymol
    conda deactivate
    echo
    echo
    echo "this was version $version"
    read -p "Press any key to resume ..."
    echo
    echo

done
