#!/bin/bash
set -eu
mkdir ./tos_build/dist | true
cp -rf ./skeleton_distbuild ./tos_build/dist/
mkdir ./tos_web/dist | true
cp -rf ./skeleton_distweb ./tos_web/dist/

/bin/bash /var/www/base/build.sh
/bin/bash /var/www/base/bootstrap.sh

echo "nginx READY!"
/usr/sbin/nginx -g 
BASEDIR=$(cd $(dirname $0); pwd)

cd ${BASEDIR}/tos-web-rest/
npm install 
ng run main
# WAITING