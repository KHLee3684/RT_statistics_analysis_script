#!/usr/bin/python
#
# Writer: Chaerin
# Modified by KHLee 160715
# Description: It prints statistics, number and percentage of data over expected period.
# Usage: ./stat_data.py <data file> <task_period> <input_unit> <output_unit> <Label>
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

if len(sys.argv) < 6 :
    print "usage : %s <data file> <task_period> <input_unit> <output_unit> <Label>"%sys.argv[0]
    sys.exit(-1)

tag_name = os.path.splitext(os.path.split(sys.argv[1])[1])[0]
file_data_input = open(sys.argv[1], 'r')
script_path = os.path.join(os.path.split(__file__)[0], "")

period = float(sys.argv[2])
input_unit = sys.argv[3]
output_unit = sys.argv[4]
graph_label = sys.argv[5]
scaler = float(unit_convert[input_unit]) / unit_convert[output_unit]

input_data = []

over_1percent = 0
over_10percent = 0
data_size = 0
average = 0
minimum = 9999999999
maximum = -9999999999
stdev = 0

# create arrays
while 1:
    _line = file_data_input.readline().splitlines()
    if _line == [] : break
    data_size = data_size + 1
    _line = float(_line[0])
    input_data.append(_line)

    if (_line > 1.01 * period) or (_line < 0.99 * period):
        over_1percent = over_1percent + 1
    if (_line > 1.1 * period) or (_line < 0.9 * period):
        over_10percent = over_10percent + 1

average = numpy.mean(input_data)
minimum = min(input_data)
maximum = max(input_data)
stdev = numpy.std(input_data)

over_1percent_pct = float(over_1percent) / data_size * 100
over_10percent_pct = float(over_10percent) / data_size * 100

print "=========== result ==========="
print "data file name: %s"%(os.path.split(sys.argv[1])[1])
print "data size: %s"%(data_size)
print "task period: %s%s"%(period * scaler, output_unit)
print "tag name: %s"%(tag_name)
print ""
print "avg: %s"%(average * scaler)
print "min: %s"%(minimum * scaler)
print "max: %s"%(maximum * scaler)
print "stdev: %s"%(stdev * scaler)
print "data out of 1%%: %s (%s%%)"%(over_1percent, round(over_1percent_pct, 5))
print "data out of 10%%: %s (%s%%)"%(over_10percent, round(over_10percent_pct, 5))

# prepare plot file
file_frame_template = open(script_path + "frame_plot_template.gplot", 'r')
frame_template = file_frame_template.read()
file_frame_template.close()

_xrange = data_size
_xtics = int(round(_xrange / 6, -4))

_yrange_min = minimum
_yrange_max = maximum
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

frame_template = frame_template % {
    "xrange": str(_xrange),
    "xtics": str(_xtics),
    "yrange_min": str(_yrange_min * scaler),
    "yrange_max": str(_yrange_max * scaler),
    "ytics": str(_ytics * scaler),
    "unit": output_unit,
    "file_name" : sys.argv[1],
    "tag_name": tag_name,
    "scaler": "{:10.10f}".format(scaler),
    "label" : graph_label,
    "period" : str(period * scaler) + output_unit,
}

file_frame_plot = open(tag_name + "_frame_plot.gplot", 'w')
file_frame_plot.write(frame_template)
file_frame_plot.close()
