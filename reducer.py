#!/usr/bin/env python

from operator import itemgetter
import sys
from datetime import datetime, time

hvac = {}
bldgs = {}
bldgTimes = {}
bldgTemps = {}

#Partitoner
for line in sys.stdin:
    line = line.strip()
    date, time, targetTemp, actualTemp, system, systemAge, buildingID = line.split('\t')

   # Absolute Value the difference in target/actual temp readings.
    if system in hvac:
        hvac[system].append(abs(float(targetTemp)-float(actualTemp)))
    else:
        hvac[system] = []
        hvac[system].append(abs(float(targetTemp)-float(actualTemp)))

   # Check if time of recording to be in between work day.     
    if buildingID in bldgs:
        workHrs = datetime.strptime(time, '%H:%M:%S')
        beginTime = datetime.strptime("9:00:00", '%H:%M:%S')
        endTime = datetime.strptime("17:00:00", '%H:%M:%S')
        if workHrs >= beginTime and workHrs <= endTime:
            bldgs[buildingID].append(float(actualTemp))
            bldgTimes[buildingID].append(time)
            bldgTemps[buildingID].append(float(actualTemp))
    else:
        workHrs = datetime.strptime(time, '%H:%M:%S')
        beginTime = datetime.strptime("9:00:00", '%H:%M:%S')
        endTime = datetime.strptime("17:00:00", '%H:%M:%S')
        if workHrs >= beginTime and workHrs <= endTime:
            bldgs[buildingID] = []
            bldgs[buildingID].append(float(actualTemp))
            bldgTimes[buildingID] = []
            bldgTemps[buildingID] = []
            bldgTimes[buildingID].append(time)
            bldgTemps[buildingID].append(float(actualTemp))
                
#Reducer
# Turns all differences into one average.
print 'Sys\tAvg. Temperature Difference'
for system in hvac.keys():
    tempDiffAvg = sum(hvac[system])*1.0 / len(hvac[system])
    print '%s\t%s' % (system, tempDiffAvg)
    hvac[system] = []
    hvac[system].append(tempDiffAvg)

# Sort top 3 highest values, and print.
hvac_keys = sorted(hvac, key=hvac.get, reverse=True)[:3]
print '\nWorst Three HVAC Units:'
print 'Sys\tAvg. Temperature Difference'
for system in hvac_keys:
    print '%s\t%s' % (system, hvac[system][0])

# Average Temperature & Sort!
print '\nBldg\tAvg. Temperature'
for buildingID in bldgs.keys():
    tempAvg = sum(bldgs[buildingID])*1.0 / len(bldgs[buildingID])
    print '%s\t%s' % (buildingID, tempAvg)
    bldgs[buildingID] = []
    bldgs[buildingID].append(tempAvg)

bldgs_keys = sorted(bldgs, key=bldgs.get, reverse=True)[:3]
print '\nHottest Three Buildings:'
print 'Bldg\tAvg. Temperature'
for buildingID in bldgs_keys:
    print '%s\t%s' % (buildingID, bldgs[buildingID][0])

# Hottest Building Times
print '\nHottest Three Building\'s Recorded Times & Temperatures:'
print 'Bldg\tTimes\tTemperatures'
for buildingID in bldgs_keys:
    for x in range(len(bldgTimes[buildingID])):
        if x == 0:
            print '%s\t%s\t%s' % (buildingID, bldgTimes[buildingID][x], bldgTemps[buildingID][x])
        else:
            print '%s\t%s\t%s' % ('', bldgTimes[buildingID][x], bldgTemps[buildingID][x])
