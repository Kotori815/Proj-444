import bilibili_api as bili
import random, re, json
from tqdm import tqdm
from util import Extractor, outputPath

# get users
print("reading user list")
with open(outputPath + "users_all.json", 'r') as f:
    user_list = json.load(f)
    user_list = list(user_list.keys())
print("load {} users".format(len(user_list)))

# for each user, get the subscribed bangumi
extract_bangumi = Extractor('"season_id": ')
user_bangumi = dict()
bangumi_set = dict()
print('=====================================================')
print('Requesting subscribing bangumi information')
for i, user in tqdm(enumerate(user_list)):
    bangumi_g = bili.user.get_bangumi_g(uid=user)
    temp = list()
    try:
        for bangumi in bangumi_g:
            bangumi_info = json.dumps(bangumi)
            season_id = extract_bangumi.get_info_s(bangumi_info)
            temp.append(season_id)
            # recording the bangumi found
            bangumi_set[season_id] = True
    except bili.exceptions.BilibiliApiException as e:
        if e.code == 412:
            # too much access, rejected by server
            print("Getting error code 412")
            break
        elif e.code == 53013:
            # user not publishing subscribing bangunmi
            user_bangumi[user] = []
            continue

    user_bangumi[user] = temp

print('=====================================================')
print('Collecting {} users, {} bangumi'.format(i, len(bangumi_set)))
with open(outputPath + "user2video.json", 'w') as f:
    print("writing subscribings")
    json.dump(user_bangumi, f)
