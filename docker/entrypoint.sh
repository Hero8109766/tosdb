#!/bin/bash
set -eu

/bin/bash /var/www/base/build.sh

/bin/bash /var/www/base/bootstrap.sh

echo "nginx READY!"
/usr/sbin/nginx -g 
BASEDIR=$(cd $(dirname $0); pwd)

cd ${BASEDIR}/tos-web-rest/
npm install 
ng run main
# WAITING