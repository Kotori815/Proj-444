import bilibili_api as bili
import random, re, json, tqdm
# import pickle as pkl
from generation.util import Extractor, outputPath

start_list = [31374926, 8275216, 325045503, 5394044, 10426409]
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
        print('=====================================================')
        print("expand layer {} with {} users in waiting list".format(i+1, len(current_layer)))
        s1, l = len(user_set), 0

        for user in tqdm.tqdm(current_layer):
            if user_set.get(user):
                continue

            get_cnt += 1
            followings = bili.user.get_followings_raw(uid=user)
            followings_info = json.dumps(followings)
            follow_list = extrac_uid.get_info_list(followings_info)

            follow_network[user] = follow_list[:10]
            next_layer += follow_list[:10]
            user_set[user] = True

            l += len(follow_list)

        print("{} new users, {} new followings".format(len(user_set) - s1, l))
        current_layer, next_layer = next_layer, list()
except:
    # too much accessing (about 500) the server, access denied for 
    # the following hour
    print("Getting error code 412")
    if random.random() < 0.1:
        print("Uncle Chen is watching you")

print('=====================================================')
print("times of accessing API {}".format(get_cnt))
with open(outputPath + "users_all.json", 'w') as f:
    print("Wrinting {} users".format(len(user_set)))
    json.dump(list(user_set.keys()), f)
with open(outputPath + "followings.json", 'w') as f:
    print("Wrinting {} followings".format(l))
    json.dump(follow_network, f)
