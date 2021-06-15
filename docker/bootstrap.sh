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
cp -rf ${BASEDIR}/tos-build/dist/assets/js/* ./dist/assets/js/
#cp -rf ${BASEDIR}/tos-build/dist/* ./dist/

#cp -rn ../skeleton_distweb/* ./dist/

# merge

echo "Done."
