#!/bin/bash
set -eu
BASEDIR=/var/www/base/
cd ${BASEDIR}
REPATCH=0
if [ $# -ge 1 ]; then
REPATCH=$1
fi
echo "ToS database cron job start."

cd ${BASEDIR}/tos-parser/src

python3 main.py kTOS ko 0 0
python3 main.py iTOS en 0 0

parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} ${REPATCH} 0 :::: ../.././injectionlist_representative_without_itosktos.tsv 

python3 main.py iTOS pt 0 0
python3 main.py iTOS de 0 0
python3 main.py iTOS th 0 0 
python3 main.py iTOS ru 0 0

# search
cd ${BASEDIR}/tos-search/
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 
# sitemap
cd ${BASEDIR}/tos-sitemap/
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 


echo "Done."
