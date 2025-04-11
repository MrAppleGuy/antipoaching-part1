# %%
import folium
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import math

# %%
from geopy.geocoders import ArcGIS

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
for point in points:
    folium.Marker(location = [point.latitude, point.longitude], 
                  popup = [point.latitude, point.longitude], 
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
folium.Marker(location = [points[0].latitude, points[0].longitude], 
                  popup = [points[0].latitude, points[0].longitude], 
                  icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
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
def makeDistMatrix(points):
    numPoints = len(points)
    matrix = np.zeros((numPoints, numPoints))

    for i in range(numPoints):
        for j in range(i+1, numPoints):
            dist = distance(points[i], points[j])
            matrix[i][j] = dist
            matrix[j][i] = dist

    return matrix
distanceMatrix = makeDistMatrix(points)

# %%
def nearestPointAlgorithm(points, startPoint, distanceMatrix):
    numPoints = len(points)
    visited = [False for _ in range(numPoints)]
    unvisited = set(range(numPoints))
    path = [startPoint]
    visited[0] = True
    currentPoint = 0

    while len(path) < numPoints:
        nearestPoint = None
        nearestDistance = math.inf
        for point in range(numPoints):
            if not visited[point]:
                distance = distanceMatrix[currentPoint][point]
                if distance < nearestDistance:
                    nearestPoint = point
                    nearestDistance = distance
        currentPoint = nearestPoint
        path.append(currentPoint)
        visited[currentPoint] = True

    return path

# %%
nearestPoints = nearestPointAlgorithm(points, 0, distanceMatrix)
nearestPointPath = [points[index] for index in nearestPoints]
nearestPointPath.append(points[0])
totalDistance(nearestPointPath)

# %%
for point in points:
    folium.Marker(
        location=[point.latitude, point.longitude],
        popup=(point.latitude, point.longitude),
        icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
polylineCoordinates = [(point.latitude, point.longitude) for point in nearestPointPath]
folium.PolyLine(polylineCoordinates, color='green').add_to(Map)
    
Map

# %%
def twoOptInefficient(points, maxIterationsWithoutImprovement):
    bestDistance = totalDistance(points)
    iterationsWithoutImprovement = 0
    count = 0
    
    while iterationsWithoutImprovement < maxIterationsWithoutImprovement:
        improved = False
        for i in range(1, len(points) - 1):
            for j in range(i + 1, len(points)):
                count += 1
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
    print(count)
    return points

# %%
path = twoOptInefficient(points, 10)
path.append(points[0])
print(totalDistance(path))

# %%
def twoOpt(points, maxIterationsWithoutImprovement):
    iterationsWithoutImprovement = 0
    count = 0
    while iterationsWithoutImprovement < maxIterationsWithoutImprovement:
        improved = False
        for i in range(1, len(points) - 1):
            for j in range(i + 1, len(points)):
                count += 1
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
                a = oldDistance - newDistance

                oldTotalDis = totalDistance(points)
                newTotalDis = totalDistance(newPath)
                b = oldTotalDis - newTotalDis
                
                if abs(a - b) > 0.000001:
                    print ("error " + str(a - b))
                
                #print(oldDistance)
                #print(newDistance)
                if newDistance < oldDistance:
                    points = newPath
                    improved = True
                    iterationsWithoutImprovement = 0
                if not improved:
                    iterationsWithoutImprovement += 1
    print(count)
    return points

# %%
path2 = twoOpt(nearestPointPath, 10)
path2.append(points[0])
print(totalDistance(path2))

# %%
pointPath = [[point.latitude, point.longitude] for point in path]
pointPath.append(points[0])

# %%
Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)
for point in points:
    folium.Marker(
        location=[point.latitude, point.longitude],
        popup=(point.latitude, point.longitude),
        icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
polylineCoordinates = [(point.latitude, point.longitude) for point in path]
folium.PolyLine(polylineCoordinates, color='green').add_to(Map)
folium.Marker(location = [points[0].latitude, points[0].longitude], 
                  popup = [points[0].latitude, points[0].longitude, 0], 
                  icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
    
Map

# %%
Map = folium.Map(location=[points[0].latitude, points[0].longitude], zoom_start=12)

# %%
for point in points:
    folium.Marker(
        location=[point.latitude, point.longitude],
        popup=(point.latitude, point.longitude),
        icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
polylineCoordinates = [(point.latitude, point.longitude) for point in path2]
folium.PolyLine(polylineCoordinates, color='green').add_to(Map)
folium.Marker(location = [points[0].latitude, points[0].longitude], 
                  popup = [points[0].latitude, points[0].longitude, 0], 
                  icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
    
Map

# %%


