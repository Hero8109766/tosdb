#!/bin/bash
set -eu
cd /var/www/base/

BASEDIR=/var/www/base/
cd ${BASEDIR}
mkdir ./tos-build/dist | true
cp -rf ./skeleton_distbuild/* ./tos-build/dist/
mkdir ./tos-web/dist | true
cp -rf ./skeleton_distweb/* ./tos-web/dist/


/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh


# search
cd ${BASEDIR}/tos-search/
npm install
npm run main jTOS

echo "nginx READY!"
/usr/sbin/nginx 

cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js
# WAITING