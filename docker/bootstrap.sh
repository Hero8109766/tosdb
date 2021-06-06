#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=$(cd $(dirname $0); pwd)

# build up!
cd ${BASEDIR}/tos-web/
mkdir ./dist/ | true
rm -r  ./dist/* | true
ng build

# merge
cp -Rln ../tos-build/dist/* ./dist/ 

# copy
echo "Copying"

echo "Done."
