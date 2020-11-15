import bilibili_api as bili
import random
import re
import json

user_list = []
me = 31374926

mid_pattern = re.compile(r'"mid": \d*')

my_following = bili.user.get_followings_g(me)

for user in my_following:
    