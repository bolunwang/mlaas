reset
load 'style_small.gnu'

set output './eps/twitter_kmeans_ari.eps'

set yrange [-0.1:0.5]
set ytics -0.1, 0.1, 0.5
#set ytics 0.975, 0.04, 0.99
#set xrange [1:11]
#set yrange [0:1]
# set ytics 0, 10000000, 100000000
set xtics font "Helvetica, 24"
set ylabel 'Adjusted Rand Index'

#set style circle radius graph 0.005
#set key left top Left
#set key font "Helvetica,26"
unset key

#plot '../plot_files/part1_@#$_pkt_loss.txt' using 1:2 with lines  lw 8 lt 1 lc rgb 'black' title 'TCP Flow 1', \
#	'../plot_files/part1_@#$_pkt_loss.txt' using 1:3 with lines  lw 8 lt 5  lc rgb 'blue' title 'TCP Flow 2',\
#	'../plot_files/part1_@#$_pkt_loss.txt' using 1:4 with lines  lw 8 lt 4 lc rgb 'red' title 'CBR Flow'
#exit

set boxwidth 0.5
set style fill pattern border
plot "./plot_data/twitter_k_means_ars.txt" using 1:3:xtic(2) with boxes lt -1 lw 2 lc rgb '#990000' fillstyle pattern 7