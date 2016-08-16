reset
#experiment 3(compare with different ratio): ipinyou Season 3

set term postscript eps enhanced
set output "./pic/e3-2.eps"

set rmargin 0.5
set lmargin 10
set tmargin 1.0

set yrange [3000:8000]
set ylabel "MSE"
set ylabel font ", 23"
set xlabel "simulated ratio"
set xlabel font ", 23"

#set key horiz
set key right top
set key font ",23"

unset tics
set ytics 3000,1000,8000
set ytics font ",23"

set xtics ('0.167' 0, '0.333' 1, '0.500' 2, '0.667' 3, '0.833' 4) #//rotate by -45
set xtics font ",23"

set style histogram clustered gap 2  

plot './data/e3-2.dat' using 1 title 'LR' with histogram ls 5 fs pattern 1, '' using 2 title 'CLR' with histogram ls 5 fs pattern 4, '' using 3 title 'Mix' with histogram ls 5 fs pattern 2, '' using 4 title 'GammaCLR' with histogram ls 5 fs pattern 6 
