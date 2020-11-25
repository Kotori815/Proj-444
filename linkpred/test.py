import json

dataset_path = "./dataset/"
with open(dataset_path + "video2video.json", 'r') as f:
    net = json.load(f)

count = {}
for u in net.keys():
    count[u] = count.get(u, 0) + 1
    for v in net[u]:
        count[v] = count.get(v, 0) + 1

print(count)
# print(list(dict.fromkeys(count.values())))

