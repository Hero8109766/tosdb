#!/bin/bash
set -eu
cd /var/www/base/

BASEDIR=/var/www/base/
cd ${BASEDIR}

mkdir ./tos-build/dist | true
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
mkdir ./tos-web/dist | true
cp -rn ./skeleton_distweb/* ./tos-web/dist/

/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh



echo "nginx READY!"
/usr/sbin/nginx 

cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js
# WAITING