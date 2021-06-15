#!/bin/bash
set -eu
cd /var/www/base/

BASEDIR=/var/www/base/
cd ${BASEDIR}


#cp -rn ./tos-build/dist/* ./tos-web/dist/
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
cp -rn ./skeleton_distweb/* ./tos-build/dist/

/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh

#cp -rn ./tos-build/dist/* ./tos-web/dist/
#cp -rn ./skeleton_distbuild/* ./tos-web/dist/
#cp -rn ./skeleton_distweb/* ./tos-web/dist/


echo "nginx READY!"
/usr/sbin/nginx 

cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js
# WAITING