#!/usr/bin/env python
import sys

titleLine = True

# input comes from STDIN (standard input)
for line in sys.stdin:
    line = line.strip()
    line = line.split(",")

    if titleLine:
        titleLine = False
    
    elif len(line) >= 7:
        date = line[0]
        time = line[1]
        targetTemp = line[2]
        actualTemp = line[3]
        system = line[4]
        systemAge = line[5]
        buildingID = line[6]

        print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (date,time,targetTemp,actualTemp,system,systemAge,buildingID)
