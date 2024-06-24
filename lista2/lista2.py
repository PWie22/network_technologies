import networkx as nx
import numpy as np
import matplotlib.pyplot as mplot
import random as rand

class Edge:
    # every edge has its source, end and capacity
    def __init__(self, source, end, capacity):
        self.source = source
        self.end = end
        self.c = capacity

# global variables

# Function that finds an edge with given ends and returns its capacity
def findC(x:int, y:int, eList:list)->int:
    for edge in eList:
        if edge.source==x and edge.goal==y:
            return edge.c
    return 0    

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
    for u, v in g.edges():
        a = aValues[u-1][v-1]
        c = findC(u,v,edgeList)
        x = (c/m - a)
        # if flow for the edge is equal or smaller than zero, then the error is raised - the upper limit has been exceed
        if(x <= 0):
            return -1 # error code
        sum += a/x
    return sum/GValue

# function to count an average capacity of an edge - created just to count it once
'''def countAverageCapacity(eList:list)->float:
    average = 0
    for edge in eList:
        average += edge.c
    return average/len(eList)'''

numbOfNodes = 20
numbOfEdges = 29
m = 12000 # an average size of a package in bits
Tmax = 0.03 # maximal delay allowed for a package

# to są wartości przepustowości, jakie ja dodaję każdej krawędzi
values = np.array([1400000,1500000,1700000,1600000,1450000])
#values = np.array([1500000,1600000,1800000,1700000,1550000])
#values = np.array([2000000,2100000,1900000,1800000,1950000])

edgeList = [] # auxiliary list to store capacities
i = 1
k = 0
while(i < 20):
    edge = Edge(i,i+1,values[k%5])
    edgeList.append(edge)
    k += 1
    i += 1
edgeList.append(Edge(1,19,values[0]))
edgeList.append(Edge(1,15,values[1]))
edgeList.append(Edge(2,14,values[2]))
edgeList.append(Edge(2,6,values[3]))
edgeList.append(Edge(3,8,values[4]))
edgeList.append(Edge(4,12,values[0]))
edgeList.append(Edge(6,17,values[1]))
edgeList.append(Edge(7,10,values[2]))
edgeList.append(Edge(9,13,values[3]))
edgeList.append(Edge(10,20,values[4]))

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
matrix = np.ndarray(shape=(20,20), dtype=int)
# wartości, jakie wpiszę do macierzy natężeń
numbers = np.array([1,2,3,4,1])
#numbers = np.array([2,3,3,4,2])
#numbers = np.array([2,4,5,5,2])

# wstawianie wartości do macierzy natężeń i wyliczenie G
i = 0
GValue = 0
while(i<20):
    k = i
    matrix[i][k] = 0
    #k = k + 1
    while(k<20):
        k += 1
        value = k%5
        GValue = GValue + 2*value
        matrix[i][k] = numbers[value]
        matrix[k][i] = numbers[value]
        #k = k + 1
    i = i + 1

counter = 0
reliability = 0
while counter < 100:
    # tworzenie grafu
    checker = 0
    g = nx.Graph()
    i = 1
    while(i<=20):
        g.add_node(i)
        i += 1

    # dodanie krawędzi do grafu tak, żeby w sumie było 29
    i = 1
    while(i<20):
        g.add_edge(i,i+1)
        i += 1
    g.add_edges_from([(1,19),(1,15),(2,14),(2,6),(3,8),(4,12),(6,17),(7,10),(9,13),(10,20)])

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

    # usuwanie losowych krawędzi
    for u, v in g.edges():
        randNumb = rand.random()
        if randNumb>0.99:
            g.remove_edge(u,v)

    # funkcja znajdująca wszystkie najkrótsze ścieżki
    shortestPaths = nx.shortest_path(g)

    # sprawdzenie, czy graf jest spójny;
    # wykorzystałam fakt, że jeżeli graf jest spójny to funkcja shortest_path
    # zwróci mi 20 list o długości 20 każda, więc tutaj przechodzę w pętli po wszystkich tych listach
    # i sprawdzam ich długość, jeżli jakaś jest krótsza niż dwadzieścia, to ustawiam checker na -1
    for key1 in shortestPaths.keys():
        if len(shortestPaths[key1]) < 20:
            print('Network is disconnected.')
            checker = -1
            break

    # jeżli checker jest nadal równy 0 to znaczy, że graf jest spójny
    if checker == 0:
        # tablica z wartościami a(e)
        aValues = np.zeros(shape=(20,20), dtype=int)
        # tutaj wywołuję funkcję countA dla każdej ścieżki, jaką znalazła mi funkcja shortest_path
        # i wyliczam wartości do macierzy aValues
        for key1 in shortestPaths.keys():
            for key in shortestPaths[key1].keys():
                countA(shortestPaths[key1][key])

        # tu obliczam T średnie
        tValue = countT()

        # tu sprawdzam, czy wartoSC T średnie jest mniejsza, bądź równa T max oraz czy jest większa niż -1
        # bo jeżeli jest -1 to znaczy, że funkcja countT zwróciła błąd, czyli, że została przekroczona
        # przepustowość dopuszczalna
        if tValue > -1 and tValue <=Tmax:
            reliability += 1
        else:
            print('Error ',tValue)
            pass

    shortestPaths.clear()
    counter += 1

# na końcu liczę niezawodność sieci w stu próbach
print('Reliability: ',reliability/100)
