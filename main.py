

import rtree
import numpy
import geopandas as gp
import folium
import os
from shapely.geometry import Polygon,Point,LineString
import pandas

def extractingCoordinatesFromDataset(dataset_path,numberOfBreakPoint,bBox):
    ptrDataset = open(dataset_path)
    mainArray = []
    count = 0

    for eachLine in ptrDataset:
        if numberOfBreakPoint == count:
            print("BREAK POINT")
            break
        withoutNewLine = eachLine.split("\n")
        newList = withoutNewLine[0].split(";")
        floatLatitude = float(newList[3])
        floatLongitude = float(newList[4])
        if bBox[0]<floatLatitude<bBox[2] and bBox[1]<floatLongitude<bBox[3]:
            mainArray.append(newList)
        count += 1

    df = pandas.DataFrame(data=mainArray,columns=["Source_ID","Date","Altitude","Latitude","Longitude","Speed","Angle"])

    return df, mainArray


# idx = rtree.index.Index()
# left, bottom, right, top = (0.0, 0.0, 1.0, 1.0)
# idx.insert(0, (left, bottom, right, top))
#
# print(list(idx.intersection((1.0, 1.0, 2.0, 2.0))))
# print(list(idx.intersection((1.0000001, 1.0000001, 2.0, 2.0))))
#
# idx.insert(1, (left, bottom, right, top))
# print(list(idx.nearest((1.0000001, 1.0000001, 2.0, 2.0), 1)))



## Getting Data with Bounding Box

box = (39.878259,32.774105,39.918492,32.851095) ## for points

bbox = (
    32.774105 , 39.878259, 32.851095 ,39.918492 ## for lineStrings l b r t
)

roads = gp.read_file("ShapeFiles/gis_osm_roads_free_1.shp",bbox=bbox)

df, main_array = extractingCoordinatesFromDataset("./Dataset/Trafik0701.txt",1000000,bBox=box)



## Creating RTree

rTree = rtree.index.Index()

for idx,row in roads.iterrows():
    boundingBox = row["geometry"].bounds

    rTree.insert(int(row["osm_id"]),boundingBox)

resultantArray = []

for eachRow in main_array:
    newPoint = Point(float(eachRow[4]), float(eachRow[3]))
    geometry_buffered = newPoint.buffer(0.0002)
    fids = [i for i in rTree.intersection(geometry_buffered.bounds)]


    for fid in fids:
        newRow = []
        flat_list = []
        specificRow = roads.loc[roads['osm_id'] == str(fid)]
        geometry_land = specificRow['geometry']
        geometry = geometry_land.to_numpy()[0]
        buffered = geometry.buffer(0.0001)
        if buffered.contains(newPoint):
            # a = list(rTree.nearest(geometry.bounds,1))[0]
            ff = roads.loc[roads['osm_id'] == str(fid)]
            ff = ff.to_numpy().tolist()[0]
            newRow.append(eachRow)
            newRow.append(ff)
            for each in newRow:
                for item in each:
                    flat_list.append(item)
            resultantArray.append(flat_list)
            break

# print(resultantArray)

resultantDataFrame = pandas.DataFrame(data=resultantArray,columns=["Source_ID","Date","Altitude","Latitude","Longitude","Speed","Angle",'osm_id', 'code', 'fclass', 'name', 'ref', 'oneway', 'maxspeed',
        'layer', 'bridge', 'tunnel', 'geometry'])




resultantDataFrame.to_csv('data1.csv')




print(rTree)




# print(rTree.leaves())
# print(rTree.get_bounds)


# Step 1 Class olustur
# Step 2 ekle hepsini
# Step 3 gps pointi ile rTree boxlari intersectle
# Step 4 en yakini al
# Step 5 joinle


count = 0

# for eachRow in main_array:
#     newPoint = Point(float(eachRow[4]), float(eachRow[3]))
#     geometry_buffered = newPoint.buffer(0.01)
#
#     # fids = [i for i in rTree.intersection(geometry_buffered.bounds)]
#
#     fids = [i for i in rTree.nearest(geometry_buffered.bounds, 1)]
#
#     if count % 1000 == 0:
#         print(count)
#         print(fids)
#
#     for fid in fids:
#         newRow = []
#         flat_list = []
#         specificRow = roads.loc[roads['osm_id'] == str(fid)]
#
#         newRow.append(eachRow)
#         newRow.append(specificRow)
#         for each in newRow:
#             for item in each:
#                 flat_list.append(item)
#         resultantArray.append(flat_list)
#
#     count += 1
