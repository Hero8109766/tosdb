#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=/var/www/base/

# build up!
cd ${BASEDIR}/tos-web/
rm -r ./dist/* | true
ng build --optimization=false --source-map
cd ${BASEDIR}/tos-build/
cp -rf ../tos-web/dist/* ./dist/

# merge

echo "Done."
