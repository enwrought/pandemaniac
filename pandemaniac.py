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
G.add_nodes_from(nodes)
for node in nodes:
    G.add_edges_from((node, neighbor) for neighbor in jData[node])



# Choose seeds based on highest betweenness centrality
betweenness = nx.betweenness_centrality(G)
seeds = sorted(betweenness, 
               key=lambda node: betweenness[node], 
               reverse=True)[0:numSeeds]

    
### Write the chosen seeds to an output file
# Get the name of the outfile from the infile
jInd = fileName.find(".json")
outName = fileName[0 : jInd]
# Time to write
outFile = open(outName, 'w')
for i in xrange(50):
    for j in xrange(numSeeds):
        outFile.write("%s\n" % str(seeds[j]))
        
outFile.close()
