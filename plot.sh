#!/bin/bash

# plik the messages per day using gnuplot

gnuplot << EOF
set term "pdf" size 50cm,10cm font "Sans,8"
set output "zevs_messages_perday.pdf"

set timefmt "%Y-%m-%d"
set xdata time
set format x "%Y-%m-%d"
set grid

set xtics rotate
set xtics 172800
set mxtics 2

set title "ZEVS (frequency 82Hz) messages per day, as received at Jacek/SQ5BPF QTH Warsaw/KO02md"
set ylabel "ZEVS Messages per day"

plot 'zevs_messages_perday.txt'  using 1:2 with impulses notitle
EOF

