reset
#experiment 2(compare with Wush): ipinyou Season 2

set term postscript eps enhanced
set output "./pic/e2-1.eps"

set rmargin 0.5
set lmargin 10
set tmargin 0.5

set yrange [1500:3100]
set ylabel "MSE"
set ylabel font ", 23"
set xlabel "Date"
set xlabel font ", 23"

set key horiz
set key right top
set key font ",20"

unset tics
set ytics 1500,500,3000
set ytics font ",23"

set xtics ('6/7' 0, '6/8' 1, '6/9' 2, '6/10' 3, '6/11' 4, '6/12' 5) #//rotate by -45
set xtics font ",23"

set style histogram clustered gap 2  

plot './data/e2-1.dat' using 1 title 'LR' with histogram ls 5 fs pattern 1, '' using 2 title 'CLR' with histogram ls 5 fs pattern 4, '' using 3 title 'Mix' with histogram ls 5 fs pattern 2, '' using 4 title 'GammaCLR(I:10)' with histogram ls 5 fs pattern 6, '' using 5 title 'GammaCLR(I:50)' with histogram ls 5 fs pattern 7, '' using 6 title 'GammaCLR(I:100)' with histogram ls 5 fs pattern 5
