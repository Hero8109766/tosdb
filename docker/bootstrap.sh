#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=/var/www/base/

# build up!
cd ${BASEDIR}/tos-web/
#mkdir ./dist/ | true
#rm -r  ./dist/* | true
cp -rn ../tos-build/dist/* ./src/
cp -rn ../skeleton_distbuild/* ./src/
cp -rn ../skeleton_distweb/* ./src/



ng build

# merge

echo "Done."
