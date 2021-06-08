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

# merge

# copy


echo "Done."
