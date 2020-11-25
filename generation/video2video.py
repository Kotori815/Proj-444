import bilibili_api as bili
import random, json, tqdm
from util import Extractor, outputPath

start_list = ['BV12f4y1v7LJ', 'BV13K4y1j7Za', 'BV1Qi4y1L7es', 
              'BV1ev411r7vb', 'BV1cy4y167pb', 'BV1pf4y1q7uu', 
              'BV19t4y1e7vm', 'BV18K4y1Z7Xy', 'BV19p4y167Uk', 
              "BV1Bp4y1r7cY"]
            #   'BV1rr4y1F7c3',  'BV1tD4y1X7q2', 
            #   'BV1bD4y1X7bX', 'BV1LD4y1R76G', 'BV1hK4y1j7F1', 
            #   'BV145411V7kc', 'BV1Cy4y1q7Zo', 'BV1ev411t7Q7', 
            #   'BV1gV41117k6', 'BV1mK4y1j7xx', 'BV1Yp4y1r7wk', 
            #   'BV1ap4y1r75F', 'BV1CD4y1X7Jj', 'BV1iK411V7N2', 
            #   'BV1R541137mE', 'BV1qA411x71g', 'BV1Xt4y1a7Uo', 
            #   'BV1Eb411u7Fw', 'BV1yr4y1F79P', 'BV1pa411w7jQ']
# Choosen from bilibili technology site rankings 20/11/19 and 20/11/25
dig_depth = 3
expand_coef = 10
# The starting videos and parameters are manually chosen 
# so that the network has 1 component

relate_network = dict()             # following edges
video_set = dict()                   # record all the users expanded
current_layer, next_layer = start_list, list()
# users waiting to be expanded in this and next round

break_flag = False
get_cnt = 0
try:
    for i in range(1, dig_depth):
        print('=====================================================')
        print("expand layer {} with {} videos".format(i, len(current_layer)))
        s1, l = len(video_set), 0

        for j, video in tqdm.tqdm(enumerate(current_layer)):
            if video_set.get(video):
                continue

            get_cnt += 1
            relate_info = bili.video.get_related(bvid=video)
            relate = [u['bvid'] for u in relate_info[:expand_coef]]

            relate_network[video] = relate
            next_layer += relate
            video_set[video] = True

            l += len(relate)

        print("get {} new recommendations, {} new videos, ".format(l, len(video_set) - s1))
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