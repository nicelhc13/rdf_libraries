#!/bin/bash

T_UNICODES=( 'FFFA' 'FFFB' 'FFFC'
             'FFFD' 'FFFE' 'FFFF'
             'FFF0' 'FFF1' 'FFF2'
             'FFF3' 'FFF4' 'FFF5'
             'FFF6' 'FFF7' 'FFF8'
             'FFF9' )

DIR=$1

SED_PARAM=""
for ucode in ${T_UNICODES[@]}
do
  echo $ucode
  # Literal unicode or encoded string as UTF8.
  SED_PARAM+="\\\u"${ucode}"|"$(echo -ne '\u'${ucode})"|"
#SED_PARAM+="\\u"${ucode}"|"
done

SED_PARAM=${SED_PARAM::-1}

SED_PARAM="s/(${SED_PARAM})//g"
echo $SED_PARAM

echo "Target DIR:" $1

for f in $DIR/*.nt
do
  fname=${f##*/}
  echo "Processing $fname file.."
  sed -r -i "${SED_PARAM}" $DIR$fname
  echo "sed -r -i ${SED_PARAM} $DIR$fname"
done

