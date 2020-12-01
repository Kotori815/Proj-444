import networkx as nx
import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import random

dataset_path = "./dataset/"

def read_data() -> (nx.Graph, dict):
    with open(dataset_path + "video2video_bfs.json", 'r') as f:
        vid_network = json.load(f)

    G = nx.Graph()
    bvid2index = dict() # store index instead of str in Graph

    for vid, recom_list in vid_network.items():
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

def genarate_dataset(graph: nx.Graph) -> (pd.DataFrame, nx.Graph):
    print("===================")
    # get all unlinked edges and sample from them (negative entries)
    print("generating negative entries")
    node_num = graph.number_of_nodes()
    node_list = list(graph.nodes())
    node_1, node_2 = list(), list()
    for i in tqdm(range(node_num)):
        for j in range(i):
            if not graph.has_edge(i, j):
                node_1.append(i)
                node_2.append(j)
    unlinked = pd.DataFrame({"node_1": node_1, "node_2": node_2})
    index = random.sample(range(len(node_1)), k=int(len(node_1) / 100))
    unlinked = unlinked.loc[index]
    unlinked['link'] = 0
    print("{} negative entries".format(int(len(node_1) / 100)))
    
    # get all existing edges
    print("generating positive entries")
    node_1, node_2 = list(), list()
    for u, v in graph.edges():
        node_1.append(u)
        node_2.append(v)
    linked = pd.DataFrame({"node_1": node_1, "node_2": node_2})
    # get all removeable egdes (positive entries)
    # that is, removing this edge will not disconnect the graph
    temp = linked.copy()
    initial_node_count = graph.number_of_nodes()
    omissible_links = []
    for i in tqdm(linked.index.values):
    # remove a node pair and build a new graph
        G_temp = nx.from_pandas_edgelist(linked.drop(index = i), 
                                         source= "node_1", 
                                         target= "node_2", 
                                         create_using = nx.Graph())
        # check whether removing this egde splits the graph
        if (nx.number_connected_components(G_temp) == 1) and (len(G_temp.nodes) == initial_node_count):
            omissible_links.append(i)
            temp = temp.drop(index = i)
    print("{} positive entries".format(len(omissible_links)))

    # total dataset
    data = linked.loc[omissible_links]
    data['link'] = 1
    data = data.append(unlinked[['node_1', 'node_2', 'link']])
    print("===================")
    print("Dataset info:")
    print(data['link'].value_counts())

    return data, G_temp

def process_parameters(dataset: pd.DataFrame, graph_train: nx.Graph) -> pd.DataFrame:
    node_pairs = list()
    for _, row in dataset.iterrows():
        node_pairs.append([row['node_1'], row['node_2']])

    print("calculating distance")
    distance = [nx.dijkstra_path_length(graph_train, u, v) for u, v in tqdm(node_pairs)]
    print("calculate Jaccard index  & Adamic/Adar index")
    jaccard = [j for _, _, j in tqdm(nx.jaccard_coefficient(graph_train, node_pairs))]
    adamic_adar =[a for _, _, a in tqdm(nx.adamic_adar_index(graph_train, node_pairs))]

    dataset['distance'] = distance
    dataset['jaccard'] = jaccard
    dataset['adamic_adar'] = adamic_adar

    return dataset


graph, bvid2index = read_data()
# draw_degree_hist(graph)
dataset, graph_train = genarate_dataset(graph)
dataset = process_parameters(dataset, graph_train)

