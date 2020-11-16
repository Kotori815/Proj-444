import bilibili_api as bili
import random, re, json
from tqdm import tqdm
from util import Extractor, outputPath

# get my followings generator
me = 31374926
my_following = bili.user.get_followings_g(me)

# get uids of my followings
extract_uid = Extractor('"mid": ')
following_list = list()
for user in my_following:
    user_info = json.dumps(user)
    uid = extract_uid.get_info_s(user_info)
    following_list.append(int(uid))

extract_bangumi = Extractor('"season_id": ')
user_bangumi = dict()
for user in tqdm(following_list):
    # Some users set subscribing bangumi invisible, 
    # which will raise exception when accessing.
    try:
        bili.user.get_bangumi_raw(user)
    except:
        continue

    temp = list()        
    bangumi_g = bili.user.get_bangumi_g(user)    
    for bangumi in bangumi_g:
        bangumi_info = json.dumps(bangumi)
        match = extract_bangumi.get_info_s(bangumi_info)
        temp.append(int(match))
    # If a user has no subscribing bangumi, then ignore him/her
    if len(temp):
        user_bangumi[user] = temp


output = outputPath + "user2video.json"
with open(output, 'w') as f:
    json.dump(user_bangumi, f)
