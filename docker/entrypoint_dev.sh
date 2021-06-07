#!/bin/bash
set -eu



echo "nginx READY!"
/usr/sbin/nginx -g 
BASEDIR=$(cd $(dirname $0); pwd)

cd ${BASEDIR}/tos-web-rest/
npm install 
ng run main
# WAITING