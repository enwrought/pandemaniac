import sys
import json
import networkx as nx

if len(sys.argv) < 2:
    print "No input json file"
    exit()

# Get the number of players and seeds from the file name    
# Files are in format numPlayers.numSeeds.ID.json
# Currently assumes that the json file is in the same directory as the script

fileName = sys.argv[1]
firstPeriod = fileName.find(".")
numPlayers = int(fileName[0 : firstPeriod])

secondPeriod = fileName.find(".",firstPeriod+1)
numSeeds = int(fileName[firstPeriod+1 : secondPeriod])

# Parse the input file
jInFile = open(fileName)
jStr = jInFile.read()
jData = json.loads(jStr)
nodes = jData.keys()
    
G = nx.Graph()

# Create the graph
for node in nodes:
    currentNodes = G.nodes()
    if node not in currentNodes:
        G.add_node(node)
        
    neighbors = jData[node]
    for neighbor in neighbors:
        if neighbor not in currentNodes:
            G.add_node(neighbor)
            
        G.add_edge(node, neighbor)
        
# Determine what nodes to use as seeds
# Currently this is done by finding the highest degree nodes, and then picking
# the highest degree nodes that connect to those nodes
degrees = G.degree()
v = list(degrees.values())
k = list(degrees.keys())
        
seeds = []
i = 0
while i < numSeeds and len(v) > 0:
    # Get the current highest degree node
    currMax = max(v)
    key = k[v.index(currMax)]
    v.remove(currMax)
    k.remove(key)
    
    # Get the nodes adjacent to the current highest degree node
    adjNodes = list(nx.all_neighbors(G, key))
    if len(adjNodes) <= numSeeds - i:
        # If the number of adjacent nodes is less than the number of nodes we
        # needs to satisfy the seed requirement, then just add them all to the
        # list (as long as they are not already there)
        for j in range(0, len(adjNodes)):
            if adjNodes[j] not in seeds:
                seeds.append(adjNodes[j])
                i += 1
    elif len(adjNodes) == 0:
        # This shouldn't ever be the case, but if it is...
        seeds.append(key)
        i += 1
    else:
        # Find out how many more seeds we need and get that many of the highest
        # degree adjacent nodes
        numLeft = numSeeds - i
        adjDegs = G.degree(adjNodes)
        adjDegv = list(adjDegs.values())
        adjDegk = list(adjDegs.keys())
        for j in range(0, numLeft):
            val = max(adjDegv)
            key2 = adjDegk[adjDegv.index(val)]
            if key2 not in seeds:
                seeds.append(key2)
                i += 1
            adjDegv.remove(val)
            adjDegk.remove(key2)

# Post-loop check to see that we have enough seed nodes
if i < numSeeds:
    print "Did not find enough seed nodes!"
    exit()
    
### Write the chosen seeds to an output file
# Get the name of the outfile from the infile
jInd = fileName.find(".json")
outName = fileName[0 : jInd]
# Time to write
outFile = open(outName, 'w')
for i in range(0, 50):
    for j in range(0, numSeeds):
        outFile.write(str(seeds[j]))
        outFile.write("\n")
        
outFile.close()
