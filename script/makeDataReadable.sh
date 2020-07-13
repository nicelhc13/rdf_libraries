#!/bin/bash

T_UNICODES=( 'FFFA' 'FFFB' 'FFFC'
             'FFFD' 'FFFE' 'FFFF'
             'FFF0' 'FFF1' 'FFF2'
             'FFF3' 'FFF4' 'FFF5'
             'FFF6' 'FFF7' 'FFF8'
             'FFF9' '0027' '0025'
             '0060' '00B4' '2018'
             '2019' '201C' '201D'
             '0023' '0000' '0001'
             '0002' '0003' '0004'
             '0005' '0006' '0007'
             '0008' 
             '000E' '000F' '0010'
             '0011' '0012' '0013'
             '0014' '0015' '0016'
             '0017' '0018' '0019'
             '001A' '001B' '001C'
             '001D' '001E' '001F'
             '0080' '0081'
             '0082' '0083' '0084'
             '0085' '0086' '0087'
             '0088' '0089' '008A'
             '008B' '008C' '008D'
             '008E' '008F' '0090'
             '0091' '0092' '0093'
             '0094' '0095' '0096'
             '0097' '0098' '0099'
             '009A' '009B' '009C'
             '009D' '009E' '009F')

#T_UNICODES=( '0060' )
              # control, double quote,
              # quote, percentage unicodes

DIR=$1

SED_PARAM=""
# UNICODE REPLACEMENT
for ucode in ${T_UNICODES[@]}
do
  echo $ucode
  # Literal unicode or encoded string as UTF8.
  SED_PARAM+="\\\u${ucode}|$(echo -ne '\u'${ucode})|"
done
echo "Ucode construction done .."
SED_PARAM=${SED_PARAM::-1}

# URL STARTING WITH DIGIT REPLACEMENT
SED_PARAM="s/${SED_PARAM}//g;"
SED_PARAM=${SED_PARAM}"/^_[^:]/d;" # remove URL starts from _, but not followed by :
#SED_PARAM=${SED_PARAM}"/<*\"+[^>]*>/d;" # remove URL having "
#SED_PARAM=${SED_PARAM}"/^[^(<|_|\")].*/d;"

#SED_PARAM=${SED_PARAM}"/WARN  riot/d;"
#SED_PARAM=${SED_PARAM}"/INFO  riot/d;"
#SED_PARAM=${SED_PARAM}"/<*_+[^>]*>/d;" # remove URL having _ --> it removes valid URL
SED_PARAM=${SED_PARAM}"s/<http:\\/\\/[0-9]+[^>]*>/<http:\\/\\/replaced.com>/g;"
SED_PARAM=${SED_PARAM}"s/<https:\\/\\/[0-9]+[^>]*>/<https:\\/\\/replaced.com>/g;"
SED_PARAM=${SED_PARAM}"s/<ftp:\\/\\/[0-9]+[^>]*>/<ftp:\\/\\/replaced.com>/g;"
#SED_PARAM=${SED_PARAM}"s/\[//g"
#SED_PARAM=${SED_PARAM}"s/\]//g"

#SED_PARAM=${SED_PARAM}"s/^(_)?:.*/_:/g" # replace _ to _:


echo $SED_PARAM

echo "Target DIR:" $1

#for f in $DIR/*
for f in $DIR/*.ttl
#for f in $DIR/*.nt
do
  fname=${f##*/}
  echo "Processing $fname file.."
  sed -r -E -e ${SED_PARAM} $DIR$fname > ${DIR}extract_1.nt
  #sed -i -r -E -e ${SED_PARAM} $DIR$fname
  echo "sed -r '${SED_PARAM}' $DIR$fname"
done

