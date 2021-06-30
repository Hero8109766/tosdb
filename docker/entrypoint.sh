#!/bin/bash
set -eu
cd /var/www/base/

BASEDIR=/var/www/base/
cd ${BASEDIR}

/bin/bash ${BASEDIR}/bootstrap.sh


echo "Launching tos-web-rest"
cd ${BASEDIR}/tos-web-rest/
npm install 
node src/index.js &

echo "Launching tos-reaction"

cd ${BASEDIR}/tos-reaction/
python3 app.py &

if [ -e ./_complete.sh ]; then
    sh ./_complete.sh
fi

echo "Launching nginx and WAIT"
/usr/sbin/nginx -g "daemon off;"
