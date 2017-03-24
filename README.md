# RT_statistics_analysis_script
Statistics analysis script for Real-Time experimental data

### usage
>
`
$ ./setup.sh <data file> <mode>
`<br>
>data file : your data file name<br>
>mode : "1col" or "2col" or "clean"<br>
>>1col : analysis for 1 column data<br>
>>2col : analysis for 2 column data<br>
>>clean : delete all created files<br>

>results will be created in [tag]_result directory.<br>

### you can change variables in setup.sh file :
>period : control period (input unit)<br>
>input_unit : log value's unit (s, ms, us, ns)<br>
>output_unit : result value's unit (s, ms, us, ns)<br>
>label : graph label<br>

### example
>#### for sample/1col_sample.txt data
>>check setup.sh file :<br>
`
period=0.001
`<br>
`
input_unit=s
`<br>
>>start analysis:<br>
`
$ ./setup.sh sample/1col_sample.txt 1col
`

>#### for sample/2col_sample.log data
>>check setup.sh file :<br>
`
period=1000000
`<br>
`
input_unit=ns
`<br>
>>start analysis:<br>
`
$ ./setup.sh sample/2col_sample.log 2col
`<br>
