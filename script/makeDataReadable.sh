#!/bin/bash

T_UNICODES=( 'FFFA' 'FFFB' 'FFFC'
             'FFFD' 'FFFE' 'FFFF'
             'FFF0' 'FFF1' 'FFF2'
             'FFF3' 'FFF4' 'FFF5'
             'FFF6' 'FFF7' 'FFF8'
             'FFF9' '0027' '0025'
             '0060' '00B4' '2018'
             '2019' '201C' '201D' )

#T_UNICODES=( '0060' )
              # control, double quote,
              # quote, percentage unicodes

DIR=$1

SED_PARAM=""
for ucode in ${T_UNICODES[@]}
do
  echo $ucode
  # Literal unicode or encoded string as UTF8.
  SED_PARAM+="\\\u${ucode}|$(echo -ne '\u'${ucode})|"
  #SED_PARAM+="\\\u${ucode}\|"
done

echo "Ucode construction done .."

SED_PARAM=${SED_PARAM::-1}

SED_PARAM="s/${SED_PARAM}//g"
echo $SED_PARAM

echo "Target DIR:" $1

for f in $DIR/*.ttl
#for f in $DIR/*.nt
do
  fname=${f##*/}
  echo "Processing $fname file.."
  sed -i -r ${SED_PARAM} $DIR$fname
  echo "sed -i -r '${SED_PARAM}' $DIR$fname"
done

