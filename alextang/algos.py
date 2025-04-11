from collections import defaultdict
from geopy.distance import geodesic
import numpy as np
def distance(point1, point2):
    return geodesic((point1.latitude, point1.longitude), (point2.latitude, point2.longitude)).kilometers
def christofidesTwoOpt(points, graph, maxIterationsWithoutImprovement):
    def kruskalMST(graph, numPoints):
        edges = [(i, j, graph[i][j]) for i in range(numPoints) for j in range(i + 1, numPoints) if graph[i][j] > 0]
        edges.sort(key=lambda edge: edge[2])
        parent = list(range(numPoints))
        mst = []
        for u, v, weight in edges:
            # Find parent roots
            root_u, root_v = u, v
            while parent[root_u] != root_u:
                root_u = parent[root_u]
            while parent[root_v] != root_v:
                root_v = parent[root_v]
            # Add edge if it doesn't create a cycle
            if root_u != root_v:
                mst.append((u, v, weight))
                parent[root_u] = root_v
            if len(mst) == numPoints - 1:
                break
        return mst

    def oddDegreeNodes(mst):
        degrees = defaultdict(int)
        for u, v, _ in mst:
            degrees[u] += 1
            degrees[v] += 1
        return {node for node, degree in degrees.items() if degree % 2 == 1}

    def greedyPerfectMatching(oddNodes, points):
        edges = [(i, j, distance(points[i], points[j])) for i in oddNodes for j in oddNodes if i < j]
        edges.sort(key=lambda x: x[2])
        matched = set()
        matching = []
        for u, v, dist in edges:
            if u not in matched and v not in matched:
                matching.append((u, v, dist))
                matched.update({u, v})
        return matching

    def createEulerianTour(multigraph, numPoints):
        graph = defaultdict(list)
        for u, v, _ in multigraph:
            graph[u].append(v)
            graph[v].append(u)
        currPath = [0]
        path = []
        while currPath:
            u = currPath[-1]
            if graph[u]:
                v = graph[u].pop()
                graph[v].remove(u)
                currPath.append(v)
            else:
                path.append(currPath.pop())
        return path[::-1]

    def createHamiltonianCircuit(eulerianTour):
        visited = set()
        hamiltonianCircuit = []
        for v in eulerianTour:
            if v not in visited:
                visited.add(v)
                hamiltonianCircuit.append(v)
        hamiltonianCircuit.append(hamiltonianCircuit[0])  # Close the circuit
        return hamiltonianCircuit

    def twoOpt(path, maxIterationsWithoutImprovement):
        iterationsWithoutImprovement = 0
        while iterationsWithoutImprovement < maxIterationsWithoutImprovement:
            improved = False
            for i in range(1, len(path) - 1):
                for j in range(i + 1, len(path)):
                    newPath = path.copy()
                    newPath[i:j] = path[j-1:i-1:-1]
                    oldDistance = distance(points[path[i - 1]], points[path[i]]) + distance(points[path[j - 1]], points[path[j]])
                    newDistance = distance(points[newPath[i - 1]], points[newPath[i]]) + distance(points[newPath[j - 1]], points[newPath[j]])
                    if newDistance < oldDistance:
                        path = newPath
                        improved = True
                        iterationsWithoutImprovement = 0
            if not improved:
                iterationsWithoutImprovement += 1
        return path

    numPoints = len(points)
    mst = kruskalMST(graph, numPoints)
    oddNodes = oddDegreeNodes(mst)
    matched = greedyPerfectMatching(oddNodes, points)

    # Combine MST and perfect matching
    multigraph = mst.copy()
    for u, v, weight in matched:
        multigraph.append((u, v, weight))
    eulerianTour = createEulerianTour(multigraph, numPoints)
    hamiltonianCircuit = createHamiltonianCircuit(eulerianTour)

    optimizedPath = twoOpt(hamiltonianCircuit, maxIterationsWithoutImprovement)
    optimizedPoints = [points[i] for i in optimizedPath]

    return optimizedPoints


def totalDistance(order):
    totalDistance = 0
    numPoints = len(order)
    for i in range(numPoints - 1):
        point1 = order[i]
        point2 = order[i + 1]
        distance1 = distance(point1, point2)
        totalDistance += distance1
    return totalDistance

def makeDistMatrix(points):
    numPoints = len(points)
    matrix = np.zeros((numPoints, numPoints))

    for i in range(numPoints):
        for j in range(i+1, numPoints):
            dist = distance(points[i], points[j])
            matrix[i][j] = dist
            matrix[j][i] = dist

    return matrix