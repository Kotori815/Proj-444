import bilibili_api as bili
import random, re, json, tqdm
# import pickle as pkl
from util import Extractor, outputPath

start_list = [31374926, 8275216, 325045503, 5394044, 10426409, 9164472, 38137569]
# 31374926 is me

dig_depth = 3

extrac_uid = Extractor(r'"mid": ') # uid extractor

follow_network = dict()             # following edges
user_set = dict()                   # record all the users expanded
current_layer, next_layer = start_list, list()
# users waiting to be expanded in this and next round

get_cnt = 0
try:
    for i in range(dig_depth):
        print("expand layer {}".format(i+1))
        print("total user: {}".format(len(current_layer)))
        s1, l = len(user_set), 0

        for user in tqdm.tqdm(current_layer):
            if user_set.get(user):
                continue

            followings = bili.user.get_followings_raw(user)
            get_cnt += 1
            followings_info = json.dumps(followings)
            follow_list = extrac_uid.get_info_list(followings_info)

            follow_network[user] = follow_list[:10]
            next_layer += follow_list[:10]
            user_set[user] = True

            l += len(follow_list)

        print("new user number: {}, new followings: {}".format(len(user_set) - s1, l))
        
        current_layer, next_layer = next_layer, list()
except:
    print("Getting error code 412")
    if random.random() < 0.1:
        print("Uncle Chen is watching you")

print("total get number {}".format(get_cnt))
with open(outputPath + "users_all.json", 'w') as f:
    print("Wrinting {} users".format(len(user_set)))
    json.dump(user_set, f)
with open(outputPath + "followings.json", 'w') as f:
    print("Wrinting {} followings".format(l))
    json.dump(follow_network, f)
