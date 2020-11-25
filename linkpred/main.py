import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm

dataset_path = "./dataset/"

def read_data() -> (nx.Graph, dict):
    with open(dataset_path + "video2video.json", 'r') as f:
        vid_network = json.load(f)

    G = nx.Graph()
    bvid2index = dict() # store index instead of str in Graph

    for vid, recom_list in vid_network.items():
        # if len(bvid2index) > size:
        #     break
        for v in recom_list:
            if bvid2index.get(vid) == None:
                bvid2index[vid] = len(bvid2index)
            if bvid2index.get(v) == None:
                bvid2index[v] = len(bvid2index)
            G.add_edge(bvid2index[vid], bvid2index[v])
            
    print("Graph with {} nodes and {} edges".format(G.number_of_nodes(), G.number_of_edges()))
    return G, bvid2index

def draw_degree_hist(G: nx.Graph, save: bool = False):
    degreeDict = dict()
    for vertex in G.nodes():
        deg = G.degree(vertex)
        degreeDict[deg] = degreeDict.get(deg, 0) + 1

    max_degree = max(degreeDict.keys())
    
    x = list(range(1, max_degree + 1))
    y = [degreeDict.get(i, 0) for i in x]    
    a = plt.bar(x, y)
    plt.xlabel('degree')
    plt.ylabel('times')
    if save:
        plt.savefig("degree.png")
    plt.show()

def genarate_data(graph: nx.Graph, tt_ratio: float = 0.7):
    # get all edges
    node_1, node_2 = list(), list()
    for u, v in tqdm(graph.edges()):
        node_1.append(u)
        node_2.append(v)
    linked = pd.DataFrame({"node_1": node_1, "node_2": node_2})
    
    # get all unlinked edges
    node_num = graph.number_of_nodes()
    node_list = list(graph.nodes())
    node_1, node_2 = list(), list()
    for i in tqdm(range(node_num)):
        for j in range(i):
            if not graph.has_edge(i, j):
                node_1.append(i)
                node_2.append(j)
    unlinked = pd.DataFrame({"node_1": node_1, "node_2": node_2})
    
    # get all removeable egdes
    # that is, removing this edge will not disconnect the graph
    g_temp = graph.copy()
    for edge in graph.edges():
        pass
        
graph, bvid2index = read_data()
print(nx.number_connected_components(graph))
# draw_degree_hist(graph)
genarate_data(graph)
