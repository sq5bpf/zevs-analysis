#!/bin/bash

# plot the number of minutes the 82Hz carrier was active --sq5bpf

gnuplot << EOF
set term "pdf" size 50cm,10cm font "Sans,8"
set output "zevs_activity.pdf"

set timefmt "%Y-%m-%d"
set xdata time
set format x "%Y-%m-%d"
set grid

set xtics rotate
set xtics 172800
set mxtics 2

set title "ZEVS number of minutes per day the 82Hz carrier was active, as received at Jacek/SQ5BPF QTH Warsaw/KO02md"
set ylabel "ZEVS 82Hz minutes per day"

plot 'zevs_activity.txt'  using 1:2 with impulses notitle
EOF

