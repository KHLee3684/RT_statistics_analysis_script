#!/usr/bin/python
#
# Writer: Chaerin
# Modified by KHLee 160713
# Description: It prints statistics -
#       release interval, send interval, release jitter, response time, send point.
#       And It saves statistics files for graph.
# Usage: ./statistics_analysis.py <your_data> <task_period> <tag> <input_unit> <output_unit> <Label>
# I am using this at Python version 2.7

import sys
import os.path
import math
import numpy

unit_convert = {
    "ns" : 1,
    "us" : 1000,
    "ms" : 1000000,
    "s" : 1000000000
}

if len(sys.argv) < 7 :
    print "usage : %s <your_data> <task_period> <tag> <input_unit> <output_unit> <Label>"%sys.argv[0]

file_data_input = open(sys.argv[1], 'r')
period = float(sys.argv[2])
tag_name = sys.argv[3]

input_unit = sys.argv[4]
output_unit = sys.argv[5]
graph_label = sys.argv[6]
scaler = float(unit_convert[input_unit]) / unit_convert[output_unit]

release_interval = []
send_point_interval = []
release_jitter = []
response_time = []
send_point = []

input_data = []

length = 0

release_over_1percent = 0
release_over_10percent = 0
send_over_1percent = 0
send_over_10percent = 0

# create arrays
while 1:
    _line = file_data_input.readline().splitlines()
    if _line == [] : break
    length = length + 1
    input_data.append(_line[0].split())
    
for i in range(length):
    try:
        release_interval.append(int(input_data[i+1][0]) - int(input_data[i][0]))
        send_point_interval.append(int(input_data[i+1][1]) - int(input_data[i][1]))
        release_jitter.append(int(input_data[i+1][0]) - int(input_data[i][0]) - int(period))
        response_time.append(int(input_data[i][1]) - int(input_data[i][0]))
        send_point.append(release_jitter[i] + response_time[i])
    except:
        break

# write to file
file_release_interval = open("release_interval_" + tag_name + ".txt", 'w')
file_send_point_interval = open("send_point_interval_" + tag_name + ".txt", 'w')
file_release_jitter = open("release_jitter_" + tag_name + ".txt", 'w')
file_response_time = open("response_time_" + tag_name + ".txt", 'w')
file_send_point = open("send_point_" + tag_name + ".txt", 'w')

for i in range(length):
    try:
        file_release_interval.write("%s\n"%(str(release_interval[i])))
        file_send_point_interval.write("%s\n"%(str(send_point_interval[i])))
        file_release_jitter.write("%s\n"%(str(release_jitter[i])))
        file_response_time.write("%s\n"%(str(response_time[i])))
        file_send_point.write("%s\n"%(str(send_point[i])))

        if (release_interval[i] > 1.01 * period) or (release_interval[i] < 0.99 * period) :
            release_over_1percent = release_over_1percent + 1
        if (release_interval[i] > 1.1 * period) or (release_interval[i] < 0.9 * period) :
            release_over_10percent = release_over_10percent + 1
        if (send_point_interval[i] > 1.01 * period) or (send_point_interval[i] < 0.99 * period) :
            send_over_1percent = send_over_1percent + 1
        if (send_point_interval[i] > 1.1 * period) or (send_point_interval[i] < 0.9 * period) :
            send_over_10percent = send_over_10percent + 1
    except:
        break

file_data_input.close()
file_release_interval.close()
file_send_point_interval.close()
file_release_jitter.close()
file_response_time.close()
file_send_point.close()

_release_interval_min = min(release_interval)
_release_interval_max = max(release_interval)
_send_point_interval_min = min(send_point_interval)
_send_point_interval_max = max(send_point_interval)
_release_jitter_min = min(release_jitter)
_release_jitter_max = max(release_jitter)
_response_time_min = min(response_time)
_response_time_max = max(response_time)
_send_point_min = min(send_point)
_send_point_max = max(send_point)

# statistics
print "+++++++++++++++ statistics +++++++++++++++"
print "data file name: %s"%(sys.argv[1])
print "data size: %s"%(length)
print "task period: %s%s"%(period * scaler, output_unit)
print "tag name: %s"%(tag_name)
print ""
print "<release interval>---------------------"
print "avg: %s"%(numpy.mean(release_interval) * scaler)
print "min: %s"%(_release_interval_min * scaler)
print "max: %s"%(_release_interval_max * scaler)
print "stdev: %s"%(numpy.std(release_interval) * scaler)
print "data out of 1%%: %s (%s%%)"%(release_over_1percent, round(float(release_over_1percent) / length * 100, 5))
print "data out of 10%%: %s (%s%%)"%(release_over_10percent, round(float(release_over_10percent) / length * 100, 5))
print ""
print "<send point interval>---------------------"
print "avg: %s"%(numpy.mean(send_point_interval) * scaler)
print "min: %s"%(_send_point_interval_min * scaler)
print "max: %s"%(_send_point_interval_max * scaler)
print "stdev: %s"%(numpy.std(send_point_interval) * scaler)
print "data out of 1%%: %s (%s%%)"%(send_over_1percent, round(float(send_over_1percent) / length * 100, 5))
print "data out of 10%%: %s (%s%%)"%(send_over_10percent, round(float(send_over_10percent) / length * 100, 5))
print ""
print "<release jitter>---------------------"
print "avg: %s"%(numpy.mean(release_jitter) * scaler)
print "min: %s"%(_release_jitter_min * scaler)
print "max: %s"%(_release_jitter_max * scaler)
print "stdev: %s"%(numpy.std(release_jitter) * scaler)
print ""
print "<response time>---------------------------"
print "avg: %s"%(numpy.mean(response_time) * scaler)
print "min: %s"%(_response_time_min * scaler)
print "max: %s"%(_response_time_max * scaler)
print "stdev: %s"%(numpy.std(response_time) * scaler)
print ""
print "<send point>------------------------------"
print "avg: %s"%(numpy.mean(send_point) * scaler)
print "min: %s"%(_send_point_min * scaler)
print "max: %s"%(_send_point_max * scaler)
print "stdev: %s"%(numpy.std(send_point) * scaler)

# prepare plot files
file_interval_template = open("interval_plot_template.gplot", 'r')
interval_template = file_interval_template.read()
file_interval_template.close()
file_delay_template = open("delay_plot_template.gplot", 'r')
delay_template = file_delay_template.read()
file_delay_template.close()

_xrange = length
_xtics = int(round(_xrange / 6, -4))

_yrange_min = min(_release_interval_min, _send_point_interval_min)
_yrange_max = max(_release_interval_max, _send_point_interval_max)
_yrange_min_diff = period - _yrange_min
_yrange_max_diff = _yrange_max - period
if _yrange_min_diff > _yrange_max_diff :
    _diff = _yrange_min_diff * 2
else :
    _diff = _yrange_max_diff * 2
_power = int(math.floor(math.log10(_diff)))
_diff = round(_diff + 0.4999999 * pow(10, _power), -_power)
if _diff < 0.2 * period :
    _diff = 0.2 * period
_yrange_min = (period - _diff / 2)
_yrange_max = (period + _diff / 2)
_ytics = (_diff / 10)

interval_template = interval_template % {
    "xrange": str(_xrange),
    "xtics": str(_xtics),
    "yrange_min": str(_yrange_min * scaler),
    "yrange_max": str(_yrange_max * scaler),
    "ytics": str(_ytics * scaler),
    "unit": output_unit,
    "tag_name": tag_name,
    "scaler": "{:10.10f}".format(scaler),
    "label" : graph_label,
    "period" : str(period * scaler) + output_unit,
}
_yrange_max = max(_response_time_max, _send_point_max)
_power = int(math.floor(math.log10(_yrange_max)))
_yrange_max = round(_yrange_max + 0.4999999 * pow(10, _power), -_power)
_ytics = _yrange_max / 10

delay_template = delay_template % {
    "xrange": str(_xrange),
    "xtics": str(_xtics),
    "yrange_max": str(_yrange_max * scaler),
    "ytics": str(_ytics * scaler),
    "unit": output_unit,
    "tag_name": tag_name,
    "scaler": "{:10.10f}".format(scaler),
    "label" : graph_label,
    "period" : str(period * scaler) + output_unit,
}

file_interval_plot = open("interval_plot_" + tag_name + ".gplot", 'w')
file_interval_plot.write(interval_template)
file_interval_plot.close()
file_delay_plot = open("delay_plot_" + tag_name + ".gplot", 'w')
file_delay_plot.write(delay_template)
file_delay_plot.close()
