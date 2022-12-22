#!/bin/bash


# open-source versions

declare -a versions=(2.4.0 2.5.0)

for version in "${versions[@]}"
do
    humanName=$(echo $version | sed -e 's/\./-/g')
    echo "$version -> $humanName"
    conda create -y --name pymol-$humanName -c conda-forge  python">=3.5" pandas pymol-open-source=$version
done


# schrodinger versions - older versions

declare -a versions=(2.0.7 2.1.1 2.2.3 2.3.2)

for version in "${versions[@]}"
do
    humanName=$(echo $version | sed -e 's/\./-/g')
    echo "$version -> $humanName"
    conda create -y --name pymol-$humanName -c schrodinger python">=3.5" pandas pymol=$version 
done
