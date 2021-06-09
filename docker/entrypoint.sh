#!/bin/bash
set -eu
cd /var/www/base/
BASEDIR=/var/www/base/

cd ${BASEDIR}

/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh

mkdir ./tos-build/dist | true
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
mkdir ./tos-web/dist | true
cp -rn ./skeleton_distweb/* ./tos-web/dist/


echo "nginx READY!"
/usr/sbin/nginx


cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js
# WAITING