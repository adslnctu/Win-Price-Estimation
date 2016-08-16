reset
#experiment 2(compare with Wush): ipinyou Season 3

set term postscript eps enhanced
set output "./pic/e2-2.eps"

set rmargin 0.5
set lmargin 10
set tmargin 1.0

set yrange [3000:5800]
set ylabel "MSE"
set ylabel font ", 23"
set xlabel "Date"
set xlabel font ", 23"

set key horiz
set key right top
set key font ",20"

unset tics
set ytics 3000,500,5500
set ytics font ",23"
set xtics ('10/20' 0, '10/21' 1, '10/22' 2, '10/23' 3, '10/24' 4, '10/25' 5, '10/26' 6, '10/27' 7) #//rotate by -45
set xtics font ",23"

set style histogram clustered gap 2  

plot './data/e2-2.dat' using 1 title 'LR' with histogram ls 5 fs pattern 1, '' using 2 title 'CLR' with histogram ls 5 fs pattern 4, '' using 3 title 'Mix' with histogram ls 5 fs pattern 2, '' using 4 title 'GammaCLR(I:10)' with histogram ls 5 fs pattern 6, '' using 5 title 'GammaCLR(I:50)' with histogram ls 5 fs pattern 7, '' using 6 title 'GammaCLR(I:100)' with histogram ls 5 fs pattern 5 
