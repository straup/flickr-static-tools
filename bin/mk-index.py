#!/usr/bin/env python

import re
import os
import sys
import json

if __name__ == "__main__":

    source = sys.argv[1]

    index = {}

    pat = re.compile(r'.*(_i\.json)$')

    for (root, dirs, files) in os.walk(source):

        for fname in files:    

            m = pat.match(fname)

            if not m:
                continue

            path = os.path.join(root, fname)
            fh = open(path, "r")

            info = json.load(fh)
            photo = info["photo"]
            dates = photo["dates"]

            id = photo["id"]
            id = int(id)

            secret = photo["secret"]

            title = photo["title"]
            title = title["_content"]

            taken = dates["taken"]
            taken = taken.split(" ")

            ymd = taken[0]
            ymd = ymd.replace("-", "/")

            index[id] = { "title": title, "ymd": ymd, "secret": secret }

    json.dump(index, sys.stdout, indent=2)
