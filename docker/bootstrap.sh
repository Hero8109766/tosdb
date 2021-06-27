#!/bin/bash
set -eu
echo "ToS database bootstrap start."

BASEDIR=/var/www/base/
/bin/bash ${BASEDIR}/build.sh

cd ${BASEDIR}/tos-build/
cp -rf ../tos-web/dist/* ./dist/

# merge

echo "Done."
