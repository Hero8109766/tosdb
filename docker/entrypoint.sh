#!/bin/bash
set -eu

/bin/bash /var/www/base/build.sh

/bin/bash /var/www/base/bootstrap.sh

echo "nginx READY!"
/usr/sbin/nginx -g "daemon off;"