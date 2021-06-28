#!/bin/bash
set -eu
echo "ToS database building start."

REPATCH=0
if [ $# -ge 1 ]; then
REPATCH=$1
fi
# build
BASEDIR=/var/www/base/


cd ${BASEDIR}
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
cp -rn ./skeleton_distweb/* ./tos-build/dist/
cp -rn ./supplimental_data/* ./tos-parser/input


cd ${BASEDIR}/tos-parser/src
python3 main.py iTOS en 0 1
python3 main.py kTOS ko 0 1
parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} ${REPATCH} 1 :::: ../.././injectionlist_representative_without_itosktos.tsv 

python3 main.py iTOS pt 0 1
python3 main.py iTOS de 0 1
python3 main.py iTOS th 0 1 
python3 main.py iTOS ru 0 1

# search
cd ${BASEDIR}/tos-search/
npm install --force


parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 
# sitemap
cd ${BASEDIR}/tos-sitemap/
npm install --force

parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 

# build up!
cd ${BASEDIR}/tos-web/
rm -r ./dist/* | true
ng build --optimization=false --source-map

cd ${BASEDIR}

echo "Done."
