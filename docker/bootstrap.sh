#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=/var/www/base/

# build up!
cd ${BASEDIR}/tos-web/
rm -r ./dist/* | true
ng build 
cd ${BASEDIR}/tos-web/
mkdir ./dist/ | true
mkdir ./dist/assets/ | true
mkdir ./dist/assets/js | true
cp -rf ${BASEDIR}/skeleton_distbuild/assets/js ./dist/assets/js

#cp -rn ../skeleton_distweb/* ./dist/

# merge

echo "Done."
