import json
from util import Extractor, outputPath

a = "aaaaa"

with open(outputPath + "aaa.txt", 'w') as f:
    json.dump(a, f)