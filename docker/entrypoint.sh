#!/bin/bash
set -eu
cd /var/www/base/

BASEDIR=/var/www/base/
cd ${BASEDIR}


#cp -rn ./tos-build/dist/* ./tos-web/dist/
#cp -rn ./skeleton_distbuild/* ./tos-build/dist/
#cp -rn ./skeleton_distweb/* ./tos-build/dist/

/bin/bash ${BASEDIR}/build.sh
/bin/bash ${BASEDIR}/bootstrap.sh

echo "Launching nginx"
/usr/sbin/nginx 

echo "Launching tos-web-rest"
cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js&

echo "Launching tos-reaction"

cd ${BASEDIR}/tos-reaction/
python3 app.py
# WAITING