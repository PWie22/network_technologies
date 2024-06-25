import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random as rand


# global variables
numbOfNodes = 20
numbOfEdges = 29
m = 12000 # an average size of a package in bits
Tmax = 0.03 # maximal delay allowed for a package
numberOfTrials = 100
probability = 0.99 # probability that an edge is not removed from the graph  

# Function that creates matrix A which will store values of real flow for each edge
# list - one of the lists returned by function shortest_paths
def countA(l:list):
    x = 0
    i = 0
    if len(l)==1:
        aValues[l[0]-1][l[0]-1] = 0 # this is path from a vertex to itself
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
def countT()->float:
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

# to są wartości przepustowości, jakie ja dodaję każdej krawędzi
values = np.array([1400000,1500000,1700000,1600000,1450000]) # TODO: zamiast tego losować z przedziału [1400000, 1600000]
#values = np.array([1500000,1600000,1800000,1700000,1550000])
#values = np.array([2000000,2100000,1900000,1800000,1950000])

# średnia przepustowość wykorzystana w punkcie 4
#averageC = 1532758
# krawędzie do dodania w punkcie 4
'''edgeList.append(Edge(5,10,averageC))
edgeList.append(Edge(7,9,averageC))
edgeList.append(Edge(11,17,averageC))
edgeList.append(Edge(12,20,averageC))
edgeList.append(Edge(4,15,averageC))
edgeList.append(Edge(7,19,averageC))
edgeList.append(Edge(2,9,averageC))
edgeList.append(Edge(5,19,averageC))
edgeList.append(Edge(10,14,averageC))
edgeList.append(Edge(8,18,averageC))'''

# w tej macierzy przechowuję liczby pakietów, jakie przesyłam na danej krawędzi
matrix = np.ndarray(shape=(numbOfNodes,numbOfNodes), dtype=int)
# wartości, jakie wpiszę do macierzy natężeń
numbers = np.array([1,2,3,4,1])
#numbers = np.array([2,3,3,4,2])
#numbers = np.array([2,4,5,5,2])

# wstawianie wartości do macierzy natężeń i wyliczenie G
i = 0
GValue = 0
while(i<numbOfNodes):
    k = i
    matrix[i][k] = 0
    k = k + 1
    while(k<numbOfNodes):
        #k += 1
        value = k%5
        GValue = GValue + 2*value
        matrix[i][k] = numbers[value]
        matrix[k][i] = numbers[value]
        k = k + 1
    i = i + 1

# creating graph and adding nodes
g = nx.Graph()
i = 1
while(i<=numbOfNodes):
    g.add_node(i)
    i += 1

# adding edges to connect all nodes in a circle
i = 1
while(i < numbOfNodes):
    g.add_edge(i, i+1, capacity=rand.randint(1400000, 1600000))
    i += 1
g.add_edge(1, 20, capacity=rand.randint(1400000, 1600000))

other_edges = [(1,19),(1,15),(2,14),(2,6),(3,8),(4,12),(6,17),(7,10),(9,13),(10,20)] # chosen edges to add to graph g
# adding other edges
for u, v in other_edges:
    g.add_edge(u, v, capacity=rand.randint(1400000, 1600000))

'''while(g.number_of_edges() < numbOfEdges):
    u = rand.randint(1, 20)
    v = rand.randint(1, 20)
    while(v == u):
        v = rand.randint(1, 20)
    g.add_edge(u, v, capacity=rand.randint(1800000, 2000000))'''
#nx.draw(g, with_labels=True, node_color='lightblue', node_size=200, font_size=9, font_color='black', font_weight='bold')
#plt.show()

counter = 0
reliability = 0
# variables which store informations about numbers of errors that occured
tooLongDeliveryTime = 0
tooMuchSent = 0
disconnections = 0
while counter < numberOfTrials:    

    # krawędzie do dodania w punkcie 4
    '''g.add_edge(5,10)
    g.add_edge(7,9)
    g.add_edge(11,17)
    g.add_edge(12,20)
    g.add_edge(4,15)
    g.add_edge(7,19)
    g.add_edge(2,9)
    g.add_edge(5,19)
    g.add_edge(10,14)
    g.add_edge(8,18)'''

    # list to store removed edge(s) to restore the graph for another trial
    removed_edges = []
    # removing random edges
    for u, v in g.edges():
        randNumb = rand.random()
        if randNumb > probability:
            print('u: {} v: {}'.format(u, v))
            removed_edges.append([u, v, g[u][v]["capacity"]])
            g.remove_edge(u,v)

    is_connected = nx.is_connected(g) # checking if graph is still connected

    # graph is still connected
    if is_connected:
        # finding shortest paths for every node        
        shortestPaths = nx.shortest_path(g)
        # matrix in which values of a are stored
        aValues = np.zeros(shape=(20,20), dtype=int)
        # for every path I update matrix with values of a
        for key1 in shortestPaths.keys():
            for key in shortestPaths[key1].keys():
                countA(shortestPaths[key1][key])
        
        tAvg = countT()

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
        #print('Error: Network is disconnected.')

    for u, v, c in removed_edges:
        g.add_edge(u, v, capacity=c)
    counter += 1

# counting reliability of the network
print('Reliability: ', reliability/numberOfTrials)
print('Errors occured:')
print('   - network was disconnected:                      {}'.format(disconnections))
print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))

