#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=$(cd $(dirname $0); pwd)

# insert skeleton
cd ${BASEDIR}/tos-web/
cp -Rf ../tos-build/dist/* ./dist/

# build up!
cd ${BASEDIR}/tos-web/
ng build --prod

# copy
echo "Copying"

echo "Done."
