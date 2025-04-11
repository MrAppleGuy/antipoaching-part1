# %%
import folium
import geopy
from geopy.distance import geodesic
import pandas as pd
import numpy as np
import math
from alextang.algos import makeDistMatrix
from alextang.algos import distance

# %%
class Point:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

# %%
points = []
points.clear()
csv = pd.read_csv("Coordinates.csv")
for index, row in csv.iterrows():
    latitude = row['latitude']
    longitude = row['longitude']
    points.append(Point(latitude, longitude))

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
distanceMatrix = makeDistMatrix(points)
print(distanceMatrix)

# %%
def nearestPointPath(points, startPoint, distanceMatrix):
    numPoints = len(points)
    visited = [False for _ in range(numPoints)]
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
nearestPointPath = nearestPointPath(points, 0, distanceMatrix)
Path = [points[index] for index in nearestPointPath]
Path.append(points[0])

# %%
for point in points:
    folium.Marker(location = [point.latitude, point.longitude], 
                  popup = [point.latitude, point.longitude], 
                  icon=folium.Icon(color='blue', icon='map-marker')).add_to(Map)
polyline_coordinates = [(point.latitude, point.longitude) for point in Path]
folium.PolyLine(polyline_coordinates, color='green').add_to(Map)
folium.Marker(location=[points[0].latitude, points[0].longitude],
              popup=[points[0].latitude, points[0].longitude],
              icon=folium.Icon(color='red', icon='map-marker')).add_to(Map)
Map

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
totalDistance(Path)

# %%


