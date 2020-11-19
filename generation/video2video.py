import bilibili_api as bili
import random, json, tqdm
from generation.util import Extractor, outputPath

start_list = ["BV1rr4y1F7c3"] #, 885292352, 542802265, 245278735, 457796356, 797798335, 287764576, 627792561, 927760278, 970315820]
# Choosen from bilibili technology site rankings 20/11/19 

dig_depth = 2

relate_network = dict()             # following edges
video_set = dict()                   # record all the users expanded
current_layer, next_layer = start_list, list()
# users waiting to be expanded in this and next round

get_cnt = 0
try:
    for i in range(dig_depth):
        print('=====================================================')
        print("expand layer {} with {} videos in waiting list".format(i+1, len(current_layer)))
        s1, l = len(video_set), 0

        for video in tqdm.tqdm(current_layer):
            if video_set.get(video):
                continue

            get_cnt += 1
            relate_info = bili.video.get_related(bvid=video)
            relate = [u['bvid'] for u in relate_info[:20]]

            relate_network[video] = relate
            next_layer += relate
            video_set[video] = True

            l += len(relate)

        print("{} new videos, {} new relates".format(len(video_set) - s1, l))
        current_layer, next_layer = next_layer, list()
except:
    # too much accessing (about 500) the server, access denied for 
    # the following hour
    print("Getting error code 412")
    if random.random() < 0.1:
        print("Uncle Chen is watching you")

print('=====================================================')
print("times of accessing API {}".format(get_cnt))
with open(outputPath + "video_all.json", 'w') as f:
    print("Wrinting {} videos".format(len(video_set)))
    json.dump(list(video_set.keys()), f)
with open(outputPath + "video2video.json", 'w') as f:
    print("Wrinting {} relates".format(l))
    json.dump(relate_network, f)
