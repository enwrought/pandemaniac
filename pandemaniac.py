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
# Currently this is done by simply picking the nodes with the highest degrees.
# This algorithm should definitely be improved upon.
degrees = G.degree()
v = list(degrees.values())
k = list(degrees.keys())
        
seeds = []
for i in range(0, numSeeds):
    val = max(v)
    key = k[v.index(val)]
    seeds.append(key)
    v.remove(val)
    k.remove(key)
    
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
