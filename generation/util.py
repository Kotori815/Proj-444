import bilibili_api as bili
import random
import re
import json

outputPath = "dataset/"

class Extractor():
    """
    Extract pieces from json-styled info
    """
    def __init__(self, pattern: str):
        """
        style: re Pattern object
        """
        self.pattern = re.compile(pattern + '\d*')
        self.index = len(pattern)

    def get_info_s(self, info_full: str) -> str:
        """
        Get a single piece of info from the full string
        """
        matching = re.search(self.pattern, info_full)
        # match = next(matching)
        return matching.group(0)[self.index:]

    def get_info_list(self, info_full: str) -> list:
        """
        Get a list of multiple info from the full string
        """
        if info_full == '':
            return []
        matching = re.finditer(self.pattern, info_full)
        matches = list()
        for match in matching:
            s = match.group(0)[self.index:]
            matches.append(s)
        return matches
        