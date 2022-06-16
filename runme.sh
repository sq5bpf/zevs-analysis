#!/bin/bash

# find valid ZEVS transmissions and generate a nice graph
# (c) 2022 Jacek Lipkowski SQ5BPF  <sq5bpf@lipkowski.org>


. ./settings.shlib

error() {
	echo "ERROR: $1"
	exit 1
}

### main

#uncomment the next line to download
#[ -f $ZEVS_ARCHIVE ] || curl -o $ZEVS_ARCHIVE "$ZEVS_URL"

if [ ! -d $ZEVS_DIR ]; then
	if [ -f $ZEVS_ARCHIVE ]; then
		echo "unpacking $ZEVS_ARCHIVE"
		tar xzf $ZEVS_ARCHIVE || error "error unpacking $ZEVS_ARCHIVE"
	else
		error "please download the $ZEVS_ARCHIVE file, look in the script for a hint"
	fi
fi


chmod a+x *.py *.sh

echo "running analysis..."

./parse_zevsdir.py > $FREQDETECT || error "error executing parse_zevsdir.py"

sort -n < $FREQDETECT > $FREQDETECT_SORTED

./find_zevs_transmissions.py > $ZEVS_MESSAGES || error "error running find_zevs_transmissions.py"

awk '/7 tones/ { A[$1]++ } END { for (i in A) print i " " A[i] }' $ZEVS_MESSAGES  | sort -n > $ZEVS_MESSAGES_PERDAY

./generate_all_spectrograms.sh
