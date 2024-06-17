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

tree = ET.parse(filename)
root = tree.getroot()
    
segmentBranch = root.find("Segments")

mainSplits = []
subSplits = []
mainSplitGoldsIGT = {}
mainSplitGoldsRTA = {}

for segment in segmentBranch:
    name = segment.find("Name").text    
    subSplits.append(segment)
    if name[0] != '-':
        mainSplits.append(subSplits)
        subSplits = []
        
for split in mainSplits:
    splitName = ''
    bestIGT = 0
    bestRTA = 0
    if len(split) > 1:
        splitName = re.search('{.*}',split[-1].find("Name").text).group()
        IGTDico = {}
        RTADico = {}
        for subSplit in split:
            histBranch = subSplit.find("SegmentHistory")
            for timeBranch in histBranch.findall("Time"):
                gameTimeBranch = timeBranch.find("GameTime")
                realTimeBranch = timeBranch.find("RealTime")
                if gameTimeBranch != None:
                    runId = timeBranch.get("id")
                    timeText = gameTimeBranch.text
                    timeFloat = parse_time(timeText).total_seconds()
                    if runId in IGTDico:
                        IGTDico[runId].append(timeFloat)
                    else:
                        IGTDico[runId] = [timeFloat]
                if realTimeBranch != None:
                    runId = timeBranch.get("id")
                    timeText = realTimeBranch.text
                    timeFloat = parse_time(timeText).total_seconds()
                    if runId in RTADico:
                        RTADico[runId].append(timeFloat)
                    else:
                        RTADico[runId] = [timeFloat]
        mainSplitIGTs = []
        for runId in IGTDico:      
            if len(IGTDico[runId]) == len(split):
                mainSplitIGTs.append(sum(IGTDico[runId]))
        bestIGT = timedelta(seconds = min(mainSplitIGTs))
        mainSplitRTAs = []
        for runId in RTADico:      
            if len(RTADico[runId]) == len(split):
                mainSplitRTAs.append(sum(RTADico[runId]))
        bestRTA = timedelta(seconds = min(mainSplitRTAs))
        
        
    else:
        splitName = split[0].find("Name").text
        bestIGT = parse_time(split[0].find("BestSegmentTime").find("GameTime").text)
        bestRTA = parse_time(split[0].find("BestSegmentTime").find("RealTime").text)

    mainSplitGoldsIGT[splitName] = bestIGT
    mainSplitGoldsRTA[splitName] = bestRTA
    
txtToSave = "splitName \t RTA \t IGT\n"
for name in mainSplitGoldsIGT:
    txtToSave += name + "\t" + str(mainSplitGoldsRTA[name]) + "\t" + str(mainSplitGoldsIGT[name]) + "\n"


SOB_IGT = timedelta(seconds = sum([mainSplitGoldsIGT[name].total_seconds() for name in mainSplitGoldsIGT]))
SOB_RTA = timedelta(seconds = sum([mainSplitGoldsRTA[name].total_seconds() for name in mainSplitGoldsRTA]))
print(txtToSave)
print("main split SOB RTA:\t"+str(SOB_RTA))
print("main split SOB IGT:\t"+str(SOB_IGT))
        
with open("MainSplitGold.txt",'w') as file:
    file.write(txtToSave)       
        
        
        
        
        
        