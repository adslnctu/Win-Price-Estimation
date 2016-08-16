reset
#experiment 1(parameter sensitivity): ipinyou Season 3, iteration:100

set term postscript eps enhanced
set output "./pic/e1-6.eps"

set rmargin 0.5
set lmargin 10
set tmargin 1.0

set yrange [3000:5500]
set ylabel "MSE"
set ylabel font ", 23"
set xlabel "Date"
set xlabel font ", 23"

set key horiz
set key center top
set key font ",20"

unset tics
set ytics 3000,500,5500
set ytics font ",23"
#set xtics ('Oct 20' 0, 'Oct 21' 1, 'Oct 22' 2, 'Oct 23' 3, 'Oct 24' 4, 'Oct 25' 5, 'Oct 26' 6, 'Oct 27' 7) #//rotate by -45
set xtics ('10/20' 0, '10/21' 1, '10/22' 2, '10/23' 3, '10/24' 4, '10/25' 5, '10/26' 6, '10/27' 7) #//rotate by -45
set xtics font ",23"

set style histogram clustered gap 2  

plot './data/e1-6.dat' using 1 title 'Max' with histogram ls 5 fs pattern 1, '' using 2 title 'All' with histogram ls 5 fs pattern 4, '' using 3 title 'Win' with histogram ls 5 fs pattern 2, '' using 4 title 'VarAll' with histogram ls 5 fs pattern 6
