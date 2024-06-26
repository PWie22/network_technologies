import networkx as nx
import sys

import lista2 as l2
#from lista2 import *

try:
    if(len(sys.argv) != 3):
        raise ValueError("Wrong number of arguments given. To use the program, type: \
                         python generateGraph.py <number_of_nodes> <number_of_edges>")
    
    numbOfNodes = int(sys.argv[1])
    numbOfEdges = int(sys.argv[2])
    m = 12000 # an average size of a package in bits
    Tmax = 0.03 # maximal delay allowed for a package
    numberOfTrials = 1000
    probability = 0.99 # probability that an edge is not removed from the graph  

    print("Creating matrix of flow...", end='')
    matrix, GValue = l2.createFlowMatrix(numbOfNodes)
    
    print("    Done.\nCreating graph...", end='')
    g = l2.createGraph(numbOfNodes, numbOfEdges)
    
    #nx.draw(g, with_labels=True, node_color='lightblue', node_size=200, font_size=9, font_color='black', font_weight='bold')
    #plt.show()

    print("    Done.\nTesting network...", end='')
    reliability, disconnections, tooLongDeliveryTime, tooMuchSent = l2.testNetwork(numberOfTrials, g, matrix, probability, Tmax, m, GValue)
    print("    Done.\n")
    
    # counting reliability rate of the network and presenting the results
    print('Reliability rate: ', reliability/numberOfTrials)
    print('Errors occured:')
    print('   - network was disconnected:                      {}'.format(disconnections))
    print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
    print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))

except ValueError as er:
    print("Error: {}".format(er))

# krawędzie do dodania w punkcie 4
    # other_edges = [(5,10), (7,9), (11,17), (12,20), (4,15), (7,19), (2,9), (5,19), (10,14), (8,18)]