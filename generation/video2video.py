import bilibili_api as bili
import random, json, tqdm
from util import Extractor, outputPath

start_list = ['BV1rr4y1F7c3', 'BV13K4y1j7Za', 'BV1Qi4y1L7es', 'BV1ev411r7vb', 'BV1q5411V7ST', 'BV1cy4y167pb', 'BV1pf4y1q7uu', 'BV19t4y1e7vm', 'BV18K4y1Z7Xy', 'BV19p4y167Uk']
# Choosen from bilibili technology site rankings 20/11/19 

dig_depth = 3

relate_network = dict()             # following edges
video_set = dict()                   # record all the users expanded
current_layer, next_layer = start_list, list()
# users waiting to be expanded in this and next round

break_flag = False

get_cnt = 0
try:
    for i in range(dig_depth):
        print('=====================================================')
        print("expand layer {} with {} videos in waiting list".format(i+1, len(current_layer)))
        s1, l = len(video_set), 0

        for j, video in tqdm.tqdm(enumerate(current_layer)):
            if video_set.get(video):
                continue

            get_cnt += 1
            relate_info = bili.video.get_related(bvid=video)
            relate = [u['bvid'] for u in relate_info[:20]]

            relate_network[video] = relate
            next_layer += relate
            video_set[video] = True

            l += len(relate)

        print("{} new videos, {} new recommendations".format(len(video_set) - s1, l))
        current_layer, next_layer = next_layer, list()
except:
    # too much accessing (about 500) the server, access denied for 
    # the following hour
    print("Getting error code 412")
    break_flag = True
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

if break_flag:
    with open(outputPath + "breakpoint.json", 'w') as f:
        print("Writing {} videos waiting".format(len(current_layer) + len(next_layer) - j))
        json.dump(current_layer[j:] + next_layer, f)