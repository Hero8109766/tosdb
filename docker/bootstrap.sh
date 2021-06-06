#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=$(cd $(dirname $0); pwd)


# build up!
cd ${BASEDIR}/tos-web/
ng build --prod

# insert skeleton
cd ${BASEDIR}/tos-web/
cp -Rn ../tos-build/dist/* ./dist/

# copy
echo "Copying"

echo "Done."
