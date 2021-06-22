#!/bin/bash
set -eu
echo "ToS database building start."



# build
BASEDIR=/var/www/base/


cd ${BASEDIR}
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
cp -rn ./skeleton_distweb/* ./tos-build/dist/



cd ${BASEDIR}/tos-parser/src
parallel --no-notice --colsep ' ' python3 main.py {1} {2} 0 :::: ../.././injectionlist_representative.tsv 
parallel --no-notice --colsep ' ' python3 main.py {1} {2} 0 :::: ../.././injectionlist.tsv 


# search
cd ${BASEDIR}/tos-search/
npm install

parallel --no-notice --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 
# sitemap
cd ${BASEDIR}/tos-sitemap/
npm install

parallel --no-notice --colsep ' ' npm run main {1} {2}  :::: ../injectionlist_representative.tsv 
parallel --no-notice --colsep ' ' npm run main {1} {2}  :::: ../injectionlist.tsv 

cd ${BASEDIR}

echo "Done."
