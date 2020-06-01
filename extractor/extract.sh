#!/bin/bash

infile=$1
outdir=$2
brand=$3
sql=$4

# override 65535k docker default size with tmpfs default
mem=$(($(free | awk '/^Mem:/{print $2}') / 2))k

indir=$(realpath $(dirname "${infile}"))
outdir=$(realpath "${outdir}")
infilebn=$(basename "${infile}")

docker run --rm -t -i --tmpfs /tmp:rw,size=${mem} \
  -v "${indir}":/firmware-in:ro \
  -v "${outdir}":/firmware-out \
  "firmware/extractor" \
   /home/extractor/extractor/extractor.py \
  -np \
  -b ${brand} \
  -sql ${sql} \
  /firmware-in/"${infilebn}" \
  /firmware-out


cd ${outdir}
tar -xvf $(find . -name *.tar.gz) -C ${outdir}_tar_extracted

echo "Firmware File extraction done"
