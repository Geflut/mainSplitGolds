# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 23:20:13 2024

@author: Geflut
"""

import xml.etree.ElementTree as ET
import re
import sys
from datetime import timedelta


regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>(\d+.\d+)?)$)?')


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = float(param)
    return timedelta(**time_params)




filename = sys.argv[1]          ##Change this to your file path if you like

tree = ET.parse(sys.argv[1])
root = tree.getroot()
    
segmentBranch = root.find("Segments")

mainSplits = []
subSplits = []
mainSplitGolds = {}

for segment in segmentBranch:
    name = segment.find("Name").text    
    subSplits.append(segment)
    if name[0] != '-':
        mainSplits.append(subSplits)
        subSplits = []
        
for split in mainSplits:
    splitName = ''
    bestTime = 0
    if len(split) > 1:
        splitName = re.search('{.*}',split[-1].find("Name").text).group()
        timeDico = {}
        for subSplit in split:
            histBranch = subSplit.find("SegmentHistory")
            for timeBranch in histBranch.findall("Time"):
                gameTimeBranch = timeBranch.find("GameTime")
                if gameTimeBranch != None:
                    runId = timeBranch.get("id")
                    timeText = gameTimeBranch.text
                    timeFloat = parse_time(timeText).total_seconds()
                    if runId in timeDico:
                        timeDico[runId].append(timeFloat)
                    else:
                        timeDico[runId] = [timeFloat]
        mainSplitTimes = []
        for runId in timeDico:      
            if len(timeDico[runId]) == len(split):
                mainSplitTimes.append(sum(timeDico[runId]))
        bestTime = timedelta(seconds = min(mainSplitTimes))
        
    else:
        splitName = split[0].find("Name").text
        bestTime = parse_time(split[0].find("BestSegmentTime").find("GameTime").text)

    mainSplitGolds[splitName] = bestTime
    
txtToSave = ""
for name in mainSplitGolds:
    txtToSave += name + "\t" + str(mainSplitGolds[name]) + "\n"


SOB = timedelta(seconds = sum([mainSplitGolds[name].total_seconds() for name in mainSplitGolds]))
print(txtToSave)
print("main split SOB:\t"+str(SOB))
        
with open("MainSplitGold.txt",'w') as file:
    file.write(txtToSave)       
        
        
        
        
        
        