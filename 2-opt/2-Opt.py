# %%
import folium
import geopy
#from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import math

# %%
class Point:
    def __init__(self, index, latitude, longitude):
        self.index = index
        self.latitude = latitude
        self.longitude = longitude

# %%
points = []
points.clear()
csv = pd.read_csv("Coordinates.csv")
for index, row in csv.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    points.append(Point(index, latitude, longitude))

# %%
Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)
Map

# %%
def distance(point1, point2):
    return geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).kilometers

# %%
def totalDistance(order):
    totalDistance = 0
    numPoints = len(order)
    for i in range(numPoints - 1):
        point1 = order[i]
        point2 = order[i + 1]
        distance1 = distance(point1, point2)
        totalDistance += distance1
    toBeginning = distance(order[-1], order[0])
    totalDistance += toBeginning
    return totalDistance

# %%
def twoOptInefficient(points, maxIterationsWithoutImprovement):
    bestDistance = totalDistance(points)
    iterationsWithoutImprovement = 0
    
    while iterationsWithoutImprovement < maxIterationsWithoutImprovement:
        improved = False
        for i in range(1, len(points) - 1):
            for j in range(i + 1, len(points)):
                newPath = points.copy()
                newPath[i:j] = points[j-1:i-1:-1]
                newDistance = totalDistance(newPath)
                #print(newDistance - bestDistance)
                if newDistance < bestDistance:
                    points = newPath
                    bestDistance = newDistance
                    improved = True
                    iterationsWithoutImprovement = 0
                if not improved:
                    iterationsWithoutImprovement += 1
    return points

# %%
path = twoOptInefficient(points, 10)
path.append(points[0])
print(totalDistance(path))

# %%
def twoOpt(points, maxIterationsWithoutImprovement):
    iterationsWithoutImprovement = 0
    while iterationsWithoutImprovement < maxIterationsWithoutImprovement:
        improved = False
        for i in range(1, len(points) - 1):
            for j in range(i + 1, len(points)):
                newPath = points.copy()
                
                #print('old path------------')
                #for p in newPath:
                #    print(p.index)

                newPath[i:j] = points[j-1:i-1:-1]
                #swaps the points from i inclusive to j exclusive i.e 1,2,3,4,5 where i = 1 j = 4 becomes 1,4,3,2,5

                
                #print('new ------------')
                #for p in newPath:
                #    print(p.index)
                
                oldDistance = distance(points[i - 1], points[i]) + distance(points[j - 1], points[j])
                newDistance = distance(points[i - 1], points[j - 1]) + distance(points[i], points[j])
                #a = oldDistance - newDistance

                #oldTotalDis = totalDistance(points)
                #newTotalDis = totalDistance(newPath)
                #b = oldTotalDis - newTotalDis
                
                #if abs(a - b) > 0.000001:
                #    print ("error " + str(a - b))
                
                #print(oldDistance)
                #print(newDistance)
                if newDistance < oldDistance:
                    points = newPath
                    improved = True
                    iterationsWithoutImprovement = 0
                if not improved:
                    iterationsWithoutImprovement += 1
    return points

# %%
path2 = twoOpt(points, 10)
path2.append(points[0])
print(totalDistance(path2))

# %%
for point in points:
    folium.Marker(
        location=[point.latitude, point.longitude],
        popup=(point.latitude, point.longitude),
        icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
polylineCoordinates = [(point.latitude, point.longitude) for point in path2]
folium.PolyLine(polylineCoordinates, color='green').add_to(Map)
folium.Marker(location = [points[0].latitude, points[0].longitude], 
                  popup = [points[0].latitude, points[0].longitude], 
                  icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
Map

# %%


