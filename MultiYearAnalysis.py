import pickle
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import random

yearStart=1990
years=[1999,2004,2009,2013] # Graph  up to these years will be generates
Gyr={}
for yr in years: # Graph of nodes/edges up to a given years
    Gyr[yr] = nx.Graph()

data_source='TrainSet2014_3.pkl'
fullgraph,unconnected_vertex_pairs,year_start,years_delta = pickle.load( open( data_source, "rb" ) ) # Read for file

for i in range(fullgraph.shape[0]): # Create graphs
    for yr in years:
        if (1990+fullgraph[i][2]/365)<yr: # only add node and year if the edge appear before this year
            Gyr[yr].add_node(fullgraph[i][0])
            Gyr[yr].add_node(fullgraph[i][1])
            Gyr[yr].add_edge(fullgraph[i][0], fullgraph[i][1])
            #break

##############################Draw graphs#########################################################3

def plot_degree_dist(Gyr): # Create accumative histogram of edges to nodes (how many nodes responsible to how many edges)
    for yr in years:
        G=Gyr[yr]
        degrees = np.array([G.degree(n) for n in G.nodes()]) # List of degrees per node
        percnt=np.zeros([100],dtype=np.float32)
        totalEdges=degrees.sum() # Sum of edges in the graph
        totalNodes=len(degrees) #  Sum of nodes in the graph
        #random.shuffle(degrees)
        degrees.sort()
        for i in range(len(degrees)): # Create plot of number of percentage of edges compare to percentage of nodes we
           pr=np.floor(i*100/totalNodes)
           percnt[int(pr)]+=100*degrees[i]/totalEdges
        acprcnt=percnt.copy() # accumolative prcentage
        for i in range(len(acprcnt)-1): # Transform percentage to accumative percentage (sum of previous quaries)
            acprcnt[i+1]+=acprcnt[i]
        plt.plot(acprcnt, label=str(yr))
        # print("--------------------------------")
        # print(yr)
        # for f in range(len(acprcnt)):
        #     print(f,"\t",acprcnt[f])


        #plt.plot(percnt,label=str(yr))
        plt.ylabel("Percentage of edges")
        plt.xlabel("Percentage of nodes (from low to high node degree)")
    plt.title("Accumalitive percentage")
    plt.legend()  # Add a legend.
    plt.savefig("Fig.png")
    plt.show()

plot_degree_dist(Gyr)

print("Average Clustering")  # number triangles out of total triangles
print("Year, Clustering, number of nodes")
for yr in Gyr:
    G = Gyr[yr]

    print(yr,nx.average_clustering(G),len(G.nodes))
print("transitivity") # number triangles out of total triangles
for yr in Gyr:
    G = Gyr[yr]
    print(yr,nx.transitivity(G))




# list(G.nodes)
# list(G.edges)
