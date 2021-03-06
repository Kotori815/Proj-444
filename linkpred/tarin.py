import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm
import random

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score, roc_auc_score, confusion_matrix

from read_vid2vid import *

graph, bvid2index = read_data("../dataset/video2video_bfs.json")
dataset, graph_train = genarate_dataset(graph)
# dataset = process_parameters_naive(dataset, graph_train)
dataset = process_parameters_node2vec(dataset, graph_train)

predictors = np.array(dataset.iloc[:, 3:])
response = dataset['link']
xtrain, xtest, ytrain, ytest = train_test_split(predictors, response,
                                                test_size = 0.3, 
                                                random_state = 114514)

judge = lambda x, y: 0 if x > y else 1

# logistic regression
lr = LogisticRegression(class_weight="balanced")
lr.fit(xtrain, ytrain)
predictions = lr.predict_proba(xtest)
roc_auc_score(ytest, predictions[:,1])
ypred = [judge(predictions[i,0], predictions[i,1]) for i in range(predictions.shape[0])]

# more to try