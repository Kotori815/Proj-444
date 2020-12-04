import json
import random
import numpy as np

import pmf

with open('dataset/user2video.json', 'r') as f:
    uvdict = json.load(f)

user2index = dict()
for user in uvdict.keys():
    user2index[user] = len(user2index)
len_user = len(uvdict)
vid = set()
for vlist in uvdict.values():
    vid.update(set(vlist))
len_vid = len(vid)
len_user, len_vid

R_total = np.zeros([len_user, len_vid])

video2index = dict()
for u, v_list in uvdict.items():
    for v in v_list:
        if video2index.get(v) == None:
            video2index[v] = len(video2index)
        R_total[user2index[u], video2index[v]] = 1  
        # ratings are 1/0 due to website (bilibili) limitations

R_train = R_total.copy()
R_test = list()
for i in range(R_total.shape[0]):
    for j in range(R_total.shape[1]):
        if R_train[i, j] == 1:
            if random.random() < 0.2:   # choosing 20% as testing
                R_train[i, j] = 0
                R_test.append((i,j))

K = 5
lambda_coef = 0.05
U, V =pmf.train(R_train, K, lambda_coef, 50)
M = np.round(np.dot(U.T,V))     # round the float data

err_total = np.sum(np.abs(M-R_total)) / R_total.size
print("%4f on whole rating" % err_total)
# mean absolution error (MAE) on whole rating matrix 

sm = 0
for (i,j) in R_test:
    sm += abs(M[i,j]-R_total[i,j])
err_test = sm / len(R_test)
print("%4f on whole rating" % err_test)
# mean absolution error (MAE) only considering testing data 




