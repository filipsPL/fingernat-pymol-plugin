#!/bin/bash

git pull

TAG=$(git describe --tags --abbrev=0)
REPLACEWITH="\`https:\/\/github.com\/filipsPL\/fingernat-pymol-plugin\/archive\/refs\/tags\/$TAG.zip\`"

STARTTAG="<!-- RELEASE_START -->"
ENDTAG="<!-- RELEASE_END -->"

sed -E "s/($STARTTAG)(.*)($ENDTAG)/\1$REPLACEWITH\3/" -i README.md

git add README.md
git commit -m "tag update"