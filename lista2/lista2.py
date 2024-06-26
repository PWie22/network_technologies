import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random as rand

# Function that creates matrix A which will store values of real flow for each edge
# list - one of the lists returned by function shortest_paths
def countA(aValues:np.ndarray, l:list, matrix:np.ndarray):
    x = 0
    i = 0
    if len(l)==1:
        aValues[l[0]-1][l[0]-1] = 0 # this is a path from vertex to itself
        return
    while i < len(l):
        j = i + 1
        while j < len(l):
            a = l[i] - 1
            b = l[j] - 1
            x = matrix[a][b]
            aValues[a][b] = aValues[a][b] + x
            j += 1
        i += 1
        
# Function which counts average T using the right formula.  
def countT(aValues:np.ndarray, g:nx.Graph, GValue:int, m:int)->float:
    sum = 0
    x = 0
    for u, v, data in g.edges(data=True):
        a = aValues[u-1][v-1]
        c = data["capacity"]
        x = (c/m - a)
        # if flow for the edge is equal or smaller than zero, then the error is raised - the upper limit has been exceed
        if(x <= 0):
            return -1 # error code
        sum += a/x
    return sum/GValue

def countAverageCapacity(g:nx.Graph):
    sumCapacity = 0
    for _, _, data in g.edges(data=True):
        sumCapacity += data["capacity"]
    return sumCapacity/g.number_of_edges

# values stored in matrix are numbers of packages sent between two nodes
def createFlowMatrix(numberOfNodes, whichValues=0):
    values = [[1,2,3,4,1], [2,3,3,4,2], [2,4,5,5,2]]
    matrix = np.ndarray(shape=(numberOfNodes,numberOfNodes), dtype=int)
    i = 0
    GValue = 0
    while(i<numberOfNodes):
        k = i
        matrix[i][k] = 0
        k = k + 1
        while(k<numberOfNodes):
            value = k%5
            GValue = GValue + 2*value
            matrix[i][k] = values[whichValues][value]
            matrix[k][i] = values[whichValues][value]
            k = k + 1
        i = i + 1
    return matrix, GValue

def createGraph(numberOfNodes, numberOfEdges, minCapacity=1400000, maxCapacity=1600000, randomEdges=False):
    # creating graph and adding nodes
    g = nx.Graph()
    i = 1
    while(i<=numberOfNodes):
        g.add_node(i)
        i += 1

    # adding edges to connect all nodes in a circle
    i = 1
    while(i < numberOfNodes):
        g.add_edge(i, i+1, capacity=rand.randint(minCapacity, maxCapacity))
        i += 1
    g.add_edge(1, numberOfNodes, capacity=rand.randint(minCapacity, maxCapacity))

    if randomEdges: # should add random edges
        while(g.number_of_edges() < numberOfEdges):
            u = rand.randint(1, numberOfNodes)
            v = rand.randint(1, numberOfNodes)
            while(v == u):
                v = rand.randint(1, numberOfNodes)
        g.add_edge(u, v, capacity=rand.randint(minCapacity, maxCapacity))
    else: # should add edges from the set
        other_edges = [(1,19),(1,15),(2,14),(2,6),(3,8),(4,12),(6,17),(7,10),(9,13),(10,20)] # edges chosen to add to graph g
        for u, v in other_edges:
            g.add_edge(u, v, capacity=rand.randint(minCapacity, maxCapacity))

    return g        

def testNetwork(numberOfTrials, g:nx.Graph, matrix, probability, Tmax, m, GValue):
    counter = 0
    reliability = 0
    # variables which store informations about numbers of errors occured
    tooLongDeliveryTime = 0
    tooMuchSent = 0
    disconnections = 0
    # matrix to store number of packages sent between every pair of nodes
    aValues = np.zeros(shape=(g.number_of_nodes(), g.number_of_nodes()), dtype=int)
    while counter < numberOfTrials:

        # list to store removed edges, used to quickly restore graph for another trial
        removed_edges = []
        # removing random edges
        for u, v in g.edges():
            randNumb = rand.random()
            if randNumb > probability:
                removed_edges.append([u, v, g[u][v]["capacity"]])
                g.remove_edge(u,v)

        is_connected = nx.is_connected(g) # checking if graph is still connected

        # graph is still connected
        if is_connected:
            # finding shortest paths for every node        
            shortestPaths = nx.shortest_path(g)
            # for every path I update matrix with values of a
            for key1 in shortestPaths.keys():
                for key in shortestPaths[key1].keys():
                    countA(aValues, shortestPaths[key1][key], matrix)
        
            tAvg = countT(aValues, g, GValue, m)

            # chcecking if any of the errors occured
            if tAvg == -1:
                tooMuchSent += 1
            elif tAvg > Tmax:
                tooLongDeliveryTime += 1
            else: # tAvg > -1 and tAvg <= Tmax
                reliability += 1
        
            shortestPaths.clear()
        else:
            disconnections += 1

        # restoring structures for another trial
        for u, v, c in removed_edges:
            g.add_edge(u, v, capacity=c)
        for i in range(0, g.number_of_nodes()):
            for j in range(0, g.number_of_nodes()):
                aValues[i][j] = 0
        counter += 1
    return reliability, disconnections, tooLongDeliveryTime, tooMuchSent



