from pylab import *
import numpy as np
import matplotlib.pyplot as plt
import csv
import os.path


SlopesList = {}
linkIds = []
SlopeReader = csv.reader(open('data/Partition6467LinkData.csv'))
count=0
for row in SlopeReader:
    SlopesList[row[0]]=[]
    slopes = []
    altitude = row[14].split('|')[0].split('/')[2]
    if altitude:
        SlopesList[row[0]].append(float(altitude))
    else:
        SlopesList[row[0]].append(None)
    for slope in row[16].split('|'):
        if slope:
            dist, degree = slope.split('/')
            slopes.append((float(dist), float(degree)))
    SlopesList[row[0]].append(slopes)
    linkIds.append(row[0])
    count += 1
    if count%10000==0:
        print(count)
print('Slope Loading done!')



probeReader = csv.reader(open("data\Partition6467MatchedPoints.csv"), delimiter=",")
matchedP = []
#probeIds = []
count=0
temp=(int(3496),float(51),float(9),float(200))#the initial

#ID = 3496 #the first ID
for row in probeReader:
    point = (int(row[8]),float(row[3]),float(row[4]),float(row[5]))#linkID,latitude,longitude,altitude
    esse = (row[8], float(row[5]), float(row[10]), float(row[11])) 
    count+=1
    matchedP.append(esse)
    #print(type(point))
    #only if ID is the same, the slope can be computed
    if count%10000==0:
        print(count)

print('Probe data loaded')

slopecal = {}
for matchedP in matchedP:
    LinkId = matchedP[0]
    matcheddis = matchedP[2]
    matchedAlt = matchedP[1]
    link = SlopesList[LinkId]
    refAlt = link[0]
    
    if refAlt is None or matcheddis == 0:
        degree = -1
    else:
        diffAlt = matchedAlt - refAlt
        degree = math.degrees(math.atan(diffAlt/matcheddis))
    slopecal.setdefault(LinkId, []).append((matcheddis, degree))
    
    count += 1
    if count%10000==0:
        print(count)

print("Slope calculated ")

if not os.path.isfile('slope.csv') :
    with open("data/Partition6467LinkData.csv", "r") as pp, open("slope.csv", "w") as out:
        for linkPVID,row in zip(linkIds,pp):
            line = row.strip()
            if linkPVID in link2Slope:
                linkSlope = link2Slope[linkPVID]
                linkSlope = sorted(linkSlope, key=lambda x:x[0])
                line += "," + '|'.join(['/'.join(map(str,slope)) for slope in linkSlope])

            out.write(line + "\n")
            if TESTING and idx > 10:
                break

