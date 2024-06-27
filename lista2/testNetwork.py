import sys
from colored import  fore, Style

import lista2 as l2

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


    print("{}TEST 1: NETWORK WITH DEFAULT PARAMETERS.{}".format(fore(37), Style.reset))
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


    print("\n{}TEST 2: NETWORK WITH SOME RANDOM EDGES.{}".format(fore(37), Style.reset))
    print("Testing 10 different graphs. The result is the average capacity of all 10 graphs.")
    avgReliability = 0
    for i in range(1, 11):
        print("\nCreating {} graph...".format(i), end='')
        g2 = l2.createGraph(numbOfNodes, numbOfEdges, randomEdges=True)
        print("    Done.\nTesting network...", end='')
        reliability, disconnections, tooLongDeliveryTime, tooMuchSent = l2.testNetwork(numberOfTrials, g2, matrix, probability, Tmax, m, GValue)
        print("    Done.")
        avgReliability += reliability/numberOfTrials
        print('Reliability rate: ', reliability/numberOfTrials)
        print('Errors occured:')
        print('   - network was disconnected:                      {}'.format(disconnections))
        print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
        print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))
    print("Average reliability: ", avgReliability/10)


    print("\n{}TEST 3: INCREASING VALUES IN FLOW MATRIX.{}".format(fore(37), Style.reset))
    values = [[2,2,3,4,1], [2,3,3,4,1], [2,3,3,4,2], [2,4,3,4,2], [2,4,4,4,2], [2,4,5,5,2]]
    for v in values:
        print("Creating flow matrix...", end='')
        matrix2, GValue2 = l2.createFlowMatrix(numbOfNodes, givenValues=v)
        print("    Done.\nTesting network...", end='')
        reliability, disconnections, tooLongDeliveryTime, tooMuchSent = l2.testNetwork(numberOfTrials, g, matrix2, probability, Tmax, m, GValue2)
        print("    Done.\n")
    
        print('Reliability rate: ', reliability/numberOfTrials)
        print('Errors occured:')
        print('   - network was disconnected:                      {}'.format(disconnections))
        print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
        print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))


    print("\n{}TEST 4: INCREASING CAPACITIES OF EDGES.{}".format(fore(37), Style.reset))
    minC = 1600000
    maxC = 1800000
    for i in range(1, 4):
        print("Creating graph...", end='')
        g2 = l2.createGraph(numbOfNodes, numbOfEdges, minCapacity=minC, maxCapacity=maxC)
        print("    Done.\nTesting network...", end='')
        reliability, disconnections, tooLongDeliveryTime, tooMuchSent = l2.testNetwork(numberOfTrials, g2, matrix, probability, Tmax, m, GValue)
        print("    Done.\n")
    
        print('Reliability rate: ', reliability/numberOfTrials)
        print('Errors occured:')
        print('   - network was disconnected:                      {}'.format(disconnections))
        print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
        print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))
        minC += 200000
        maxC += 200000
    

    print("\n{}TEST 5: ADDING EDGES WITH CAPACITY EQUAL TO THE AVERAGE CAPACITY OF THE INITIAL NETWORK.{}".format(fore(37), Style.reset))
    avgC = l2.countAverageCapacity(g)
    #edges = [(5,10), (7,9), (11,17), (12,20), (4,15), (7,19), (2,9), (5,19), (10,14), (8,18)]
    edges = [(5,10), (7,9), (11,17), (12,20), (4,15), (7,19), (2,9)]
    for u, v in edges:
        g.add_edge(u, v, capacity=avgC)
        print("\nTesting network...", end='')
        reliability, disconnections, tooLongDeliveryTime, tooMuchSent = l2.testNetwork(numberOfTrials, g, matrix, probability, Tmax, m, GValue)
        print("    Done.")
    
        print('Reliability rate: ', reliability/numberOfTrials)
        print('Errors occured:')
        print('   - network was disconnected:                      {}'.format(disconnections))
        print('   - too long delivery time:                        {}'.format(tooLongDeliveryTime))
        print('   - exceeded upper capacity limit of an edge:      {}'.format(tooMuchSent))


    print("\n{}TESTS FINISHED.{}".format(fore(2), Style.reset))
except ValueError as er:
    print("Error: {}".format(er))
