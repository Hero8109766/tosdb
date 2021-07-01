#!/bin/bash
set -eu
echo "ToS database bootstrap start."

BASEDIR=/var/www/base/
/bin/bash ${BASEDIR}/build.sh

cd ${BASEDIR}/tos-build/
cp -rf ../tos-web/dist/* ./dist/

# enable crontab
cd ${BASEDIR}

crontab ./tos.crontab
/etc/init.d/cron start
echo "Done."
