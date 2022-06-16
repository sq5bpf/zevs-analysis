#!/bin/bash
. ./settings.shlib

# spectrum.sh - plot the ELF spectrum from some time segment
#
# please see the following urls:
# https://klubnl.pl/wpr/en/index.php/2022/06/14/analysis-of-zevs-messages/
# https://github.com/sq5bpf/zevs-analysis
#
# (c) 2022 Jacek Lipkowski SQ5BPF <sq5bpf@lipkowski.org>



export TZ=UTC

TIMEFROM="$1"
TIMETO="$2"

if [ "$#" -lt 2 ]; then
	echo -e "\nGenerate the spectrum from the ZEVS data\n\nUsage:\n${0} date_from date_to\n\ndate_from and date_to is anything that date(1) will accept as the -d parameter\n\nexample:\n${0} '2022-02-14 9:30' '2022-02-14 12:15'"
	exit 1
fi

DATFILE=datfile
DFROM=`date +%s -d "$TIMEFROM"`
DTO=`date +%s -d "$TIMETO"`

DESCR="ZEVS spectrum at Jacek/SQ5BPF QTH Warsaw/KO02md $TIMEFROM - $TIMETO"
OUTFILE=`echo -n "spectrum_${TIMEFROM}_${TIMETO}" | tr -c 'a-zA-Z0-9_:-' _`.png

# you can change true to false if you want to save generation time and just test different gnuplot settings
if true; then
	> $DATFILE
	for i in `ls -U1 $ZEVS_DIR | awk -vL=$DFROM -vH=$DTO '($1>=L)&&($1<=H)'| sort -n`
	do
		awk -vT=$i '(NF==4) { printf( "%d %.6f %.6e\n", T, $1, $4) } END { print "" }' "$ZEVS_DIR/$i" >> $DATFILE
	done
fi

echo "Generating $OUTFILE"

gnuplot <<EOF
  set terminal png small size 1000,600
  set output "$OUTFILE"
  set ylabel 'Frequency, Hz'
  set xlabel 'UTC Day HH:MM'
  set xlabel offset 0,-4
  set palette color maxcolors 4096
  #  set pm3d at b interpolate 450,136e-6
  set view map
  set style data pm3d
  set style func pm3d
  set nokey
  set xdata time
  set timefmt '%s'
  #  set format x '%H:%M'
  set format y '%.3f'
  #  set xtics border mirror out 1800
  set xtics nomirror out rotate by 45
  #  set xrange ['$T11':'$T2']
  #  set xrange ['$T1':'$T2']
  #  set yrange [80:83.3]
  set cbrange [0:9]
  #  set xtics 900
  set mxtics 6
  set ytics 0.1
  set mytics 2
  #  set ytics border mirror out 0.2
  set format x '%m/%d %H:%M'
  set cblabel 'Relative power'
  set title '$DESCR'
  set xtics offset 0,-1.5

  splot '$DATFILE' using 1:2:(\$3 * \$3 * 1e9)
EOF

#set to true if you want to watch the pretty pictures and then remove them
if false; then
	display "$OUTFILE"
	rm "$OUTFILE"
fi
