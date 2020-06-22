#!/bin/bash
DUMP_DIR="/home/hlee/workspace/neo4j_dump"
#python3 convertToPG.py -i /home/hlee/workspace/chem2bio2rdf/semantic_network_dataset/chem2bio2rdf.txt -s 1 -o ${DUMP_DIR}/chem2bio2rdf.dump

DIR="/home/hlee/workspace/yago"
for f in $DIR/*
do
  echo "Processing $f file.."
  fname=${f##*/}
  echo python3 convertToPG.py -i $f -s 1 -o ${DUMP_DIR}/$fname.dump
  python3 convertToPG.py -i $f -s 1 -o ${DUMP_DIR}/$fname.dump
done
