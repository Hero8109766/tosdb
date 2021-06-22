#!/bin/bash
set -eu
echo "ToS database building start."



# build
BASEDIR=/var/www/base/
REGIONS=(jTOS iTOS kTOS twTOS kTEST)
#REGIONS=(jTOS)
REPATCH=0
if [ $# -ge 1 ];then
    REPATCH=$1
fi

cd ${BASEDIR}
cp -rn ./skeleton_distbuild/* ./tos-build/dist/
cp -rn ./skeleton_distweb/* ./tos-build/dist/



cd ${BASEDIR}/tos-parser/src
for region in ${REGIONS[@]} 
do
    echo ${region}
    # parse
   
    python3 main.py ${region}  ${REPATCH} 
done
# # html
# cd ${BASEDIR}/tos-html/
# npm install
# parallel npm run main ${region}
# # ->unzip
# cd ${BASEDIR}/tos-build/dist
# echo ${region,,}.zip
# if [ $(unzip -o ./${region,,}.zip) -ge 2 ];then
#     exit 1
# fi
#echo "complete"

# search
cd ${BASEDIR}/tos-search/
npm install

parallel "npm run main {1}" ::: ${REGIONS[@]}

# sitemap
cd ${BASEDIR}/tos-sitemap/
npm install
parallel "npm run main {1}" ::: ${REGIONS[@]}


cd ${BASEDIR}

echo "Done."
