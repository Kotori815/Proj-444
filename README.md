# Proj-444

## Abstract
These are codes for course project of VE444 Networks, UM-SJTU JI, partially adapted from CS224 Machine Learning with Graphs, Standford. In this prohect, we are exploring on network methods for online video recommendation. There are basically 2 ways under consideration:
- Link prediction.
  For a video entry, creating new relevant videos based on existing ones.
- Social recommendation.
  Precit a user's preferences based on the preferences of those who have relationships with him/her.

## Contents
We collect and establish our own dataset. Currently the contents are scripts for dataset generation and simple datasets. This repo (as well as the README) would be polished as the project going on.

## Acknowledgement
Some key python libraries:
- [`bilibili_api`](https://github.com/Passkou/bilibili_api): APIs to collect informations from [Bilibili](https://www.bilibili.com).
- [`NetworkX`](https://networkx.org/): A library for studying graphs and networks. It offers a wide range of graph and network-related classes and algorithms.
- [scikit-learn (`sklearn`)](https://scikit-learn.org/): Simple and efficient tools for machine learning and data analysis.
