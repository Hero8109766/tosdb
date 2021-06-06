#!/bin/bash
set -eu
echo "ToS database bootstrap start."

echo "Let's go to build up!"
BASEDIR=$(cd $(dirname $0); pwd)
# build up!
cd ${BASEDIR}/tos-web/
ng build


echo "Done."
