#!/bin/bash
set -eu
echo "ToS database building start."



# build
BASEDIR=/var/www/base/


cd ${BASEDIR}
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
cp -rn ./skeleton_distweb/* ./tos-build/dist/
cp -rn ./supplimental_data/* ./tos-parser/input


cd ${BASEDIR}/tos-parser/src
parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} 0 :::: ../.././injectionlist_representative.tsv 
#parallel --no-notice --ungroup --colsep ' ' python3 main.py {1} {2} 0 :::: ../.././injectionlist.tsv 
python3 main.py iTOS pt
python3 main.py iTOS de
python3 main.py iTOS th
python3 main.py iTOS ru

# search
cd ${BASEDIR}/tos-search/
npm install

parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 
# sitemap
cd ${BASEDIR}/tos-sitemap/
npm install

parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --ungroup --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 

cd ${BASEDIR}

echo "Done."
