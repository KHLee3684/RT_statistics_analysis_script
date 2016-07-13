#!/bin/bash

rm -f ./stat.txt

tag=sample
period=1000000
input_unit=ns
output_unit=ms
label="Sample Drive"

if [ 1 -eq $# ] ; then
	if [ "clean" == "$1" ] ; then
		rm -f ./*.txt ./*.png ./*${tag}.gplot
		exit
	fi
fi

./statistics_analysis.py ${tag}.log ${period} ${tag} ${input_unit} ${output_unit} "${label}" >> ./stat.txt
gnuplot interval_plot_${tag}.gplot
gnuplot delay_plot_${tag}.gplot
