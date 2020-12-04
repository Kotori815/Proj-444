# Proj-444

## Abstract
These are codes for course project of VE444 Networks, UM-SJTU JI, partially adapted from CS224 Machine Learning with Graphs, Standford. In this prohect, we are exploring on network methods for online video recommendation. There are basically 2 ways under consideration:
- Link prediction.
  For a video entry, creating new relevant videos based on existing ones.
- Social recommendation.
  Precit a user's preferences based on the preferences of those who have relationships with him/her.

## Contents
- `dataset`: contains all the data used in his project. All are of Python `dict` class stored as `json` files.
    - `following`: following network of users. (Actually not used)
    - `user2video` & `users_all.json`: 1344 subscribed bangumis of 492 users, totally 4559 subscriptions. (for social recommendation & link predition)
    - `video2video_bfs.json` & `video_all_bfs.json`: the video recommendation network of 843 videos, totally 1060 recommendations. (for link prediction)
- `generation1`: scripts to collect Bilibili user and video info. Information is collected by Breath-first-search (BFS).
- `linkpred`: scripts and notebooks of link predictions. Linkpred is run on 
    - User-video bipartite graph
    - Whole video reommendation graph
- `social`: scripts and notebooks of social recommendation.

## Acknowledgement
Some key python libraries:
- [`bilibili_api`](https://github.com/Passkou/bilibili_api): APIs to collect informations from [Bilibili](https://www.bilibili.com).
- [`NetworkX`](https://networkx.org/): A library for studying graphs and networks. It offers a wide range of graph and network-related classes and algorithms.
- [scikit-learn (`sklearn`)](https://scikit-learn.org/): Simple and efficient tools for machine learning and data analysis.
- [`node2vec`](https://github.com/eliorc/node2vec) Python implementation for node2vec algorith.
