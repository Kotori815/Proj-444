import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt

# from 

dataset_path = "dataset/"

with open(dataset_path + "video2video.json", 'r') as f:
    vid_network = json.load(f)
# with open(dataset_path + "video_all.json", 'r') as f:
#     vid_list = json.load(f)

# start_vids = vid_list[:185] # see log

# construct graph
G = nx.Graph()
for vid, recom_list in vid_network.items():
    # if not vid in start_vids:
    for v in recom_list:
        G.add_edge(vid, v)

print(G.number_of_edges(), G.number_of_nodes())

degreeDict = {}
for vertex in G.nodes():
    degree = G.degree(vertex)
    degreeDict[degree] = degreeDict.get(degree, 0)+1
distributionList = sorted(list(degreeDict.items()), key = lambda x: int(x[0]))
x = np.array(range(1, int(distributionList[-1][0])+1))
y = []
for tem in range(1, int(distributionList[-1][0])+1):
    y.append(degreeDict.get(tem, 0))
plt.bar(x, y)
plt.xlabel('degree')
plt.ylabel('times')
plt.show()

