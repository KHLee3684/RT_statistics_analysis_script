#!/usr/bin/python
#
# Writer: Chaerin
# Description: It prints statistics, number and percentage of data over expected period.
# Usage: python ./stat_data.py ./<your_data> <task_period> <scaler>
# I am using this at Python version 2.7

import sys
import os.path
import math

period = float(sys.argv[2])
over_1percent = 0
over_10percent = 0
data_size = 0
minimum = 9999999999
maximum = -9999999999
average = 0
avg_square = 0
line_square = 0
stdev = 0

data_file = open(sys.argv[1], 'r')
scaler = float(sys.argv[3])

while 1:
    line = data_file.readline().splitlines()
    if not line: break
    if line == []: break
    line = float(line[0])
    data_size = data_size + 1

    line_square = line * line

    if(minimum > line): minimum = line
    if(maximum < line): maximum = line

    average = average * (data_size-1) + line
    average = average / data_size
    avg_square = avg_square * (data_size-1) + line_square
    avg_square = avg_square / data_size

    if (line > 1.01*period) or (line < 0.99*period):
        over_1percent = over_1percent + 1
    if (line > 1.1*period) or (line < 0.9*period):
        over_10percent = over_10percent + 1

stdev = math.sqrt(avg_square - average * average)

over_1percent_pct = float(over_1percent)/data_size * 100
over_10percent_pct = float(over_10percent)/data_size * 100

print "=========== result ==========="
print "data size: %s"%(data_size)
print "avg: %s"%(average * scaler)
print "min: %s"%(minimum * scaler)
print "max: %s"%(maximum * scaler)
print "stdev: %s"%(stdev * scaler)
print "data out of 1%%: %s (%s%%)"%(over_1percent, round(over_1percent_pct, 5))
print "data out of 10%%: %s (%s%%)"%(over_10percent, round(over_10percent_pct, 5))
