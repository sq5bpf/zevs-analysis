#!/bin/bash
# generate spectrograms from the detected messages --sq5bpf

SPECTROGRAM_DIR=spectrograms


export TZ=UTC
L=0
while read a; do
read b c d < <( echo "$a" )
let L++

e=`echo "$c" | cut -d : -f 1`

DAT1=`date +'%s' -d "$b ${e}:00"`
let DATF=DAT1-3600
let DATT=DAT1+7200

echo "$L $b $c"

DF=`date +'%Y-%m-%d %H:%M' -d "@${DATF}"`
DT=`date +'%Y-%m-%d %H:%M' -d "@${DATT}"`

./spectrum.sh "$DF" "$DT"
done < zevs_messages.txt

mkdir -p $SPECTROGRAM_DIR
mv spectrum_*.png $SPECTROGRAM_DIR


