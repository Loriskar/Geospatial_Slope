import csv
import numpy as np
import math
import os.path


maxInt = sys.maxsize
decrement = True

while decrement:
    # decrease the maxInt value by factor 10 
    # as long as the OverflowError occurs.

    decrement = False
    try:
        csv.field_size_limit(maxInt)
    except OverflowError:
        maxInt = int(maxInt/10)
        decrement = True


linkFile = open('data/Partition6467LinkData.csv')
linkSlopes = {}
linkIds = []
Reader = csv.reader(linkFile)
count=0
for row in Reader:
    linkSlopes[row[0]]=[]
    slopes = []
    altitude = row[14].split('|')[0].split('/')[2]
    if altitude:
        linkSlopes[row[0]].append(float(altitude))
    else:
        linkSlopes[row[0]].append(None)

    for slope in row[16].split('|'):
        if slope:
            dist, degree = slope.split('/')
            slopes.append((float(dist), float(degree)))
    linkSlopes[row[0]].append(slopes)
    linkIds.append(row[0])
    count += 1
    if count%10000==0:
        print(count)


matchedPointFile = open('data/Partition6467MatchedPoints.csv')
matchedPoints = []
Reader = csv.reader(matchedPointFile)
count=0
for row in Reader:
    matchedPoints.append((row[8], float(row[5]), float(row[10]), float(row[11])))
    count += 1
    if TESTING and count==10000:
        break
    if count%10000==0:
        print(count)



if(True)
    link2Slope = {}
    for matchedPoint in matchedPoints:
        linkPVID = matchedPoint[0]
        linksDistance = matchedPoint[3]
        if linksDistance > 10:
        linkSlope = linkSlopes[linkPVID]
        refAltitude = linkSlope[0]
        pointAltitude = matchedPoint[1]
        distance = matchedPoint[2]
        if refAltitude is None or distance == 0:
            degree = None
        else:
            diffAltitude = pointAltitude - refAltitude
            degree = math.degrees(math.atan(diffAltitude/distance))
            if np.absolute(degree)>8:
                degree = None
        if distance != 0 and degree:
            link2Slope.setdefault(linkPVID, []).append((distance, degree))
        count += 1
        # debug mode
        if TESTING and count==10000:
            break
        if count%10000==0:
            print(count)

print("link2Slope")
count=0
for row in link2Slope.items():
    print(row)
    print("\n")
    count+=1
    if count == 10:
        break;

