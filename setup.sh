#!/bin/bash
#
# usage : ./setup.sh <data file> <mode>
#         data file : your data file name
#         mode : "1col" or "2col" or "clean"

period=1000000
input_unit=ns
output_unit=ms
label="Sample Drive"

if [ 2 -eq $# ] ; then
	file_name=$1
	temp=${file_name%.*}
	tag=${temp##*/}
	path=${temp%/*}
	target_dir=${tag}_result

	if [ "clean" == "$2" ] ; then
		rm -rf ./${target_dir}
		exit
	fi

	if [ ! -f ${file_name} ] ; then
		echo "no file exists : ${file_name}"
		exit
	fi
	if [ ! -d ./${target_dir} ] ; then
		mkdir ${target_dir}
	fi
	cd ${target_dir}

	if [ "1col" == "$2" ] ; then
		rm -f ./${tag}_stat.txt
		../stat_data.py ../${file_name} ${period} ${input_unit} ${output_unit} "${label}" >> ./${tag}_stat.txt
		gnuplot ./${tag}_frame_plot.gplot
	elif [ "2col" == "$2" ] ; then
		rm -f ./${tag}_stat.txt
		../statistics_analysis.py ../${file_name} ${period} ${input_unit} ${output_unit} "${label}" >> ./${tag}_stat.txt
		gnuplot ./${tag}_interval_plot.gplot
		gnuplot ./${tag}_delay_plot.gplot
	else
		echo "usage : $0 <data file> <mode>"
		echo "        data file : your data file name"
		echo "        mode : \"1col\" or \"2col\" or \"clean\""
		exit
	fi
else
	echo "usage : $0 <data file> <mode>"
	echo "        data file : your data file name"
	echo "        mode : \"1col\" or \"2col\" or \"clean\""
	exit
fi
