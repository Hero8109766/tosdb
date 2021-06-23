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
parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} ${REPATCH} :::: ../.././injectionlist_representative.tsv 
#parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} 0 :::: ../.././injectionlist.tsv 

#python3 main.py iTOS en ${REPATCH}
#python3 main.py jTOS ja ${REPATCH}
#python3 main.py kTOS ko ${REPATCH}
#python3 main.py kTEST ko ${REPATCH}
#python3 main.py twTOS zh ${REPATCH}



python3 main.py iTOS pt 0
python3 main.py iTOS de 0
python3 main.py iTOS th 0
python3 main.py iTOS ru 0

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

cd ${BASEDIR}

echo "Done."
