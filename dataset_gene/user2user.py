import bilibili_api as bili
import random, re, json, tqdm
import pickle as pkl
from util import Extractor, outputPath

class Meta:
    def __init__(self):
        self.user_num = 0
        self.follow_num = 0
        self.depth = 0
        self.expand_time = 0

start_list = [31374926] #, 8275216, 325045503, 5394044, 10426409, 9164472, 38137569]
# 31374926 is me

dig_depth = 3

extrac_uid = Extractor(r'"mid": ') # uid extractor

follow_network = dict()             # following edges
user_set = dict()                   # record all the users expanded
current_layer, next_layer = start_list, list()
# users waiting to be expanded in this and next round
bili.video.get_download_url(bvid=)
try:
    for i in range(dig_depth):
        print("expand layer {}".format(i+1))
        print("total user: {}".format(len(current_layer)))
        s1, l = len(user_set), 0

        for user in tqdm.tqdm(current_layer):
            if user_set.get(user):
                continue
            
            follow_list = []
            followings_g = bili.user.get_followings_g(user)
            
            for u in followings_g:
                info = json.dumps(u)
                uid = extrac_uid.get_info_s(info)
                follow_list.append(uid)

            follow_network[user] = follow_list
            next_layer += follow_list
            user_set[user] = True

            l += len(follow_list)

        print("new user number: {}, new followings: {}".format(len(user_set) - s1, l))
        
        current_layer, next_layer = next_layer, list()
except:
    pass

with open(outputPath + "users_all.pkl", 'a') as f:
    pkl.dump(user_set, f)
with open(outputPath + "followings.pkl", 'a') as f:
    pkl.dump(follow_network, f)
