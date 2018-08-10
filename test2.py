import numpy as np
import csv
from sklearn.neighbors import NearestNeighbors
from operator import itemgetter
import os.path
from func import distance_r_n, distance_pl

# set to True to test in first 500 data points.
TESTING = True



dirPath = 'data/'
linkPath = 'Partition6467LinkData.csv'
probePath = 'Partition6467ProbePoints.csv'



probeFile = open(dirPath+probePath)
probeP = []
probeIds = []
probeReader = csv.reader(probeFile)
count=0
for row in probeReader:
    point = (float(row[3]), float(row[4]))
    probeP.append(point)
    probeIds.append(row[0])
    count += 1
    if TESTING and count == 100:
        break
    if count%10000==0:
        print(count)

print("ProbePoints Loaded ")

OP = probeP



linkFile = open(dirPath+linkPath)
linkShapes = []
linkIds = []
linkLengths = []
linkReader = csv.reader(linkFile)
count=0
for row in linkReader:
    shapes = []
    for point in row[14].split('|'):
        latitude, longitude, _ = point.split('/')
        shapes.append((float(latitude), float(longitude)))
    linkShapes.append(shapes)
    linkIds.append(row[0])
    linkLengths.append(float(row[3]))
    count+=1
    if TESTING and count==100:
        break
    if count%10000==0:
        print(count)
print("Linkshape Loaded: ")





linkMaps = dict()
count=0
for index, link in enumerate(linkShapes):
    for linkPoint in link:
        linkMaps[linkPoint] = linkMaps.get(linkPoint, [])
        #print(count,index,linkPoint,linkMaps[linkPoint])
        linkMaps[linkPoint].append(index)
    count+=1
    if TESTING and count==100:
        break
    if count%10000==0:
        print(count)

linkPoints = list(linkMaps.keys())
print("LinkMaps setup")






probePoints = np.array(probeP)
linkPoints = np.array(linkPoints)
nearestNeighbors = NearestNeighbors(n_neighbors=100, algorithm="kd_tree").fit(linkPoints)
potentialLinks = nearestNeighbors.kneighbors(probePoints, return_distance=False)
potentialLinks = [set([bel for lat, lon in linkPoints[pl]for bel in linkMaps[lat, lon]]) for pl in potentialLinks]


print("potentialLinks found ")







if(True):
    probe2Links = []
    count=0
    for probe, links in zip(OP, potentialLinks):
        linkDis = dict()
        count+=1
        if count%10000==0:
            # break
            print(count)

        for linkId in links:
            linkpoint = np.asarray(linkShapes[linkId])
            probepoint = np.asarray(probe)
            link_dis,min_idx = distance_pl(probepoint,linkpoint)
            # record distance < 100 links
            if link_dis < 100:
                linkDis[linkId] = link_dis
        if len(linkDis) == 0:
            probe2Links.append(None)
        else:
            probe2Link = min(linkDis.items(), key=itemgetter(1))
            probe2Links.append(probe2Link)
    

print("probetoLinks matched ")


if(True):
    drivingInfo = []
    for i, (probe, link, pid) in enumerate(zip(OP, probe2Links, probeIds)):
        if link is not None:
            linkId, linkDistance = link
            #print('before',linkShapes[linkId],probe)
            linkpoint = np.asarray(linkShapes[linkId])
            probepoint = np.asarray(probe)
            linkDistance,minidx = distance_pl(probepoint,linkpoint)
            linkV = np.array(linkShapes[linkId][minidx + 1]) - np.array(linkShapes[linkId][minidx])

            cos = -100
            if i > 0 and probeIds[i - 1] == pid:
                porbeV  =  np.array(probe) - np.array(OP[i - 1])
                linkV /= np.linalg.norm(linkV)
                porbeV /= np.linalg.norm(porbeV)
                cos = np.dot(linkV, porbeV)

            if i < len(probe) - 1 and probeIds[i + 1] == pid:
                porbeV  =  np.array(OP[i + 1]) - np.array(probe)
                linkV /= np.linalg.norm(linkV)
                porbeV /= np.linalg.norm(porbeV)
                cos1 = np.dot(linkV, porbeV)
                if cos == -100 or np.abs(cos1) > np.abs(cos):
                    cos = cos1
            if cos == -100:
                cos = 1
            drivingInfo.append(cos)
        else:
            drivingInfo.append(None)
        if i % 10000 == 0:
            print (i)

print('direction found')


if(True):
    count = 0
    distances = []
    for probe, link in zip(OP, probe2Links):
        if link is not None:
            linkId, linkDistance = link
            linkpoint = linkShapes[linkId]
            distance = distance_r_n(probe,linkpoint)
            distances.append(distance)
            count += 1
            if count % 10000 == 0:
                print(count)
        else:
            distances.append(None)

print('distances calculated')



with open("data/Partition6467ProbePoints.csv", "r") as probe, open("data/Partition6467MatchedPoints.csv", "w") as out:
    for idx, (line, nearest, direct, dist) in enumerate(zip(probe, probe2Links, drivingInfo, distances)):
        if nearest is not None:
            nearest_idx, nearest_dis = nearest
            line = line.strip()
            #print('line1',line)
            dis_ref = dist[0][0]
            dis_nonref = dist[0][1]
            direction = "F" if direct > 0 else "T" 
            link_pvid = linkIds[nearest_idx]
            line += "," + ",".join([link_pvid, direction, str(dis_ref), str(dis_nonref)])
            print('line2', line)
            out.write(line + "\n")
        if TESTING and idx > 10:
            break
print('write in finished')
