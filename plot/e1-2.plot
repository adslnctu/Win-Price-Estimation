reset
#experiment 1(parameter sensitivity): ipinyou Season 2, iteration:50

set term postscript eps enhanced
set output "./pic/e1-2.eps"

set rmargin 0.5
set lmargin 10
set tmargin 1.0

set yrange [1500:3000]
set ylabel "MSE"
set ylabel font ", 23"
set xlabel "Date"
set xlabel font ", 23"

set key horiz
set key center top
set key font ",20"

unset tics
set ytics 1500,500,3000
set ytics font ",23"

#set xtics ('June 7' 0, 'June 8' 1, 'June 9' 2, 'June 10' 3, 'June 11' 4, 'June 12' 5) #//rotate by -45
set xtics ('6/7' 0, '6/8' 1, '6/9' 2, '6/10' 3, '6/11' 4, '6/12' 5)
set xtics font ",23"

set style histogram clustered gap 2  

plot './data/e1-2.dat' using 1 title 'Max' with histogram ls 5 fs pattern 1, '' using 2 title 'All' with histogram ls 5 fs pattern 4, '' using 3 title 'Win' with histogram ls 5 fs pattern 2, '' using 4 title 'VarAll' with histogram ls 5 fs pattern 6
