#!/bin/bash
set -eu

cd /root
mkdir ./tos-build/dist | true
cp -rf ./skeleton_distbuild/* ./tos-build/dist/
mkdir ./tos-web/dist | true
cp -rf ./skeleton_distweb/* ./tos-web/dist/



echo "nginx READY!"
/usr/sbin/nginx -g 
BASEDIR=$(cd $(dirname $0); pwd)

cd ${BASEDIR}/tos-web-rest/
npm install 
ng run main
# WAITING