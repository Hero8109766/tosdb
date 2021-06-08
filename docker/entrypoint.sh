#!/bin/bash
set -eu
cd /var/www/base/
BASEDIR=$(cd $(dirname $0); pwd)
cd ${BASEDIR}
mkdir ./tos-build/dist | true
cp -rf ./skeleton_distbuild/* ./tos-build/dist/
mkdir ./tos-web/dist | true
cp -rf ./skeleton_distweb/* ./tos-web/dist/


/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh

echo "nginx READY!"
/usr/sbin/nginx
BASEDIR=$(cd $(dirname $0); pwd)

cd ${BASEDIR}/tos-web-rest/
npm install 
ng run main
# WAITING