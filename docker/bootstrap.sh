#!/bin/bash
set -eu
echo "ToS database bootstrap start."

BASEDIR=/var/www/base/
/bin/bash ${BASEDIR}/build.sh

cd ${BASEDIR}/tos-build/
cp -rf ../tos-web/dist/* ./dist/

# enable crontab
cd ${BASEDIR}

cp -f ./tos.crontab /var/spool/cron/root
#/etc/init.d/cron start
cron
crontab /var/spool/cron/root

echo "Done."
