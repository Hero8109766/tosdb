#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=/var/www/base/

# build up!
cd ${BASEDIR}/tos-web/
#mkdir ./dist/ | true
#rm -r  ./dist/* | true



ng build
cp -rn ../tos-build/dist/* ./dist/
#cp -rn ../skeleton_distbuild/* ./dist/
#cp -rn ../skeleton_distweb/* ./dist/

# merge

echo "Done."
