import bilibili_api as bili
import re
import json
from util import Extractor, outputPath

me = 31374926

bili.user.get_followings_raw(31374926)