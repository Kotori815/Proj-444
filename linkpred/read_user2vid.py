import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import random, json
from node2vec import Node2Vec

"""
Read data of user 2 video raw data. Create dataset by
choosing non-existing edges as negative enties, and randomly 
removed existing edges as positive entries.

Extract features from training network. Two ways are used:
1. naive extracting: calculating pair-wise distance, jaccard
and adamic_adar index;
2. node2vec algorithm: a random-walk network node embeder
"""

dataset_path = "./dataset/"

def read_data() -> (nx.Graph, dict):
    with open(dataset_path + "user2video.json", 'r') as f:
        u2v_network = json.load(f)

    G = nx.Graph()
    user2index = dict() # store index instead of str in Graph
    video2index = dict()

    for u, v_list in u2v_network.items():
        if user2index.get(u) == None:
            user2index[u] = 2*len(user2index)
        for v in v_list:
            if video2index.get(v) == None:
                video2index[v] = 2*len(video2index) + 1
            G.add_edge(user2index[u], video2index[v])
            
    print("BiGraph with ({},{}) nodes and {} edges".format(len(user2index), len(video2index), G.number_of_edges()))
    return G, user2index, video2index

def genarate_dataset(graph: nx.Graph, users: list, videos: list) -> (pd.DataFrame, nx.Graph):
    print("===================")
    # get all unlinked edges and sample from them (negative entries)
    print("generating negative entries")
    user_list, video_list = list(), list()
    for i in tqdm(users):
        for j in videos:
            if not graph.has_edge(i, j):
                user_list.append(i)
                video_list.append(j)
    unlinked = pd.DataFrame({"users": user_list, "videos": video_list})
    index = random.sample(range(len(unlinked)), k=int(len(unlinked) / 100))
    unlinked = unlinked.loc[index]
    unlinked['link'] = 0
    print("{} negative entries".format(int(len(user_list) / 100)))

    # get all existing edges
    print("generating positive entries")
    user_list, video_list = list(), list()
    for u, v in graph.edges():
        user_list.append(u)
        video_list.append(v)
    linked = pd.DataFrame({"users": user_list, "videos": video_list})
    
    # randomly choose and remove egdes (positive entries)
    remove_index = random.sample(range(len(linked)), k=int(len(linked) / 20))
    data = linked.loc[remove_index]
    data['link'] = 1
    print("{} positive entries".format(len(remove_index)))

    # generate graph for train
    linked.drop(remove_index, inplace=True)
    G_train = nx.from_pandas_edgelist(linked,
                                      source="users",
                                      target="videos",
                                      create_using=nx.Graph())

    # total dataset
    data = data.append(unlinked[['users', 'videos', 'link']])
    print("===================")
    print("Dataset info:")
    print(data['link'].value_counts())

    return data, G_train

def process_parameters_naive(dataset: pd.DataFrame, graph_train: nx.Graph) -> pd.DataFrame:
    """
    Returns a pandas.DataFrame class, with columns\n
    | index | users | videos | link | distance | jaccard | adamic_adar |\n
    * link has only value 0 for no link and 1 otherwise.
    """
    node_pairs = list()
    for _, row in dataset.iterrows():
        node_pairs.append([row['users'], row['videos']])

    print("calculating distance")
    distance = [nx.dijkstra_path_length(graph_train, u, v) for u, v in tqdm(node_pairs)]
    print("calculate Jaccard index & Adamic/Adar index")
    jaccard = [j for _, _, j in nx.jaccard_coefficient(graph_train, node_pairs)]
    adamic_adar =[a for _, _, a in nx.adamic_adar_index(graph_train, node_pairs)]

    dataset['distance'] = distance
    dataset['jaccard'] = jaccard
    dataset['adamic_adar'] = adamic_adar

    dataset.reset_index().drop('index', axis=1)

    return dataset


def process_parameters_node2vec(dataset: pd.DataFrame, graph_train: nx.Graph, dim: int=100, walk_len: int=16, num_walks: int=50) -> pd.DataFrame:
    """
    Returns a pandas.DataFrame class, with columns\n
    | index | users | videos | dim_1 | ... | dim_n |\n
    * link has only value 0 for no link and 1 otherwise.
    """
    node2vec = Node2Vec(graph_train, dimensions=dim, walk_length=walk_len, num_walks=num_walks)
    n2w_model = node2vec.fit(window=7, min_count=1)

    embeddings = np.empty((0, dim))
    for u,v in zip(dataset['users'], dataset['videos']):
        embeddings = np.vstack((embeddings, n2w_model[str(u)] + n2w_model[str(v)]))

    colname = ["dim_{}".format(i) for i in range(dim)]
    dataset = pd.concat([dataset, 
                         pd.DataFrame(data = embeddings,
                                      columns = colname)],axis=1)
    return dataset
    

graph, bvid2index = read_data()
# draw_degree_hist(graph)
dataset, graph_train = genarate_dataset(graph)
# dataset = process_parameters_naive(dataset, graph_train)
dataset = process_parameters_node2vec(dataset, graph_train)
