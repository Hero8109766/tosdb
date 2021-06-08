#!/bin/bash
set -eu
cd /var/www/base/
BASEDIR=/var/www/base/

cd ${BASEDIR}

/bin/bash ${BASEDIR}/build.sh


/bin/bash ${BASEDIR}/bootstrap.sh

echo "nginx READY!"
/usr/sbin/nginx


cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js
# WAITING