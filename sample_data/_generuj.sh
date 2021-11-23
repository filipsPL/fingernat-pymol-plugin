#!/bin/bash

mkdir -p outputs/

python /home/filips/IIMCB/_github_/fingeRNAt/code/fingeRNAt.py -r rna.pdb -l ligands.sdf -o outputs/ -custom /home/filips/IIMCB/_github_/fingeRNAt/code/custom-interactions.yaml -detail -debug

mv outputs/DETAIL_rna.pdb_ligands.sdf_FULL.tsv DETAIL_FULL.tsv

rm -r outputs
rm ligands_OB_addedH.sdf