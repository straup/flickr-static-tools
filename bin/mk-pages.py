#!/usr/bin/env python

import re
import os
import sys
import json
import math
import shutil
import datetime

import jinja2

if __name__ == "__main__":

    source = sys.argv[1]
    index = sys.argv[2]

    #

    loader = jinja2.FileSystemLoader('../templates')
    escape = jinja2.select_autoescape(['html', 'xml'])

    env = jinja2.Environment(
        loader=loader,
        autoescape=escape
    )

    #

    fh = open(index, "r")
    index_data = json.load(fh)

    ids = []

    for id, ignore in index_data.items():
        ids.append(int(id))

    ids.sort()
    count = len(ids)
    
    nav = {}
    i = 0

    for id in ids:

        prev = None
        next = None
        
        if i != 0:
            prev = i-1

        if i < count - 1:
            next = i + 1

        if prev:

            prev_id = int(ids[prev])

            prev = index_data[ str(prev_id) ]
            prev["id"] = prev_id

        if next:

            next_id = int(ids[next])

            next = index_data[ str(next_id) ]
            next["id"] = next_id

        nav[id] = [ prev, next ]
        i += 1

    #

    photo_template = env.get_template('photo.html')

    pat = re.compile(r'.*(_i\.json)$')

    by_date = {}
    by_dow = {}

    for (root, dirs, files) in os.walk(source):

        for fname in files:    

            m = pat.match(fname)

            if not m:
                continue

            path = os.path.join(root, fname)
            fh = open(path, "r")

            info = json.load(fh)
            photo = info["photo"]

            id = photo["id"]
            id = int(id)

            prev, next = nav[id]

            dates = photo["dates"]
            taken = dates["taken"]
            taken = taken.split(" ")

            ymd = taken[0]

            dt = datetime.datetime.strptime(ymd, '%Y-%m-%d')

            body = photo_template.render(info=info, next=next, prev=prev, dt=dt)

            html = os.path.join(root, "index.html")
            page = open(html, "w")

            page.write(body.encode('utf8'))
            page.close()

            print "wrote %s" % html

            yyyymmdd = dt.strftime("%Y-%m-%d")
            yyyymm = dt.strftime("%Y-%m")
            yyyy = dt.strftime("%Y")

            for d in (yyyymmdd, yyyymm, yyyy):
                ph = by_date.get(d, [])
                ph.append(info)
                by_date[d] = ph

            dow = dt.strftime("%A")
            dow = dow.lower()

            ph = by_dow.get(dow, [])
            by_dow[dow] = ph

    #

    date_template = env.get_template('date.html')

    dates = by_date.keys()
    dates.sort()

    per_page = 24

    for d in dates:

        ids = by_date[d]
        count = len(ids)

        pages = []

        end = 0
        i = 0

        while end <  count:

            start = i * per_page
            end = start + per_page

            if end > count:
                end = count 

            pages.append(ids[start:end])
            i += 1

        page = 1

        dots = "../" * len(d.split("-"))

        dt = d.replace("-", "/")
        dt_root = os.path.join(source, dt)

        if not os.path.exists(dt_root):
            os.makedirs(dt_root)

        for photos in pages:

            prev = None
            next = None
            
            if page - 1 > 0:
                prev = page -1

            if page + 1 <= len(pages):
                next = page + 1

            for ph in photos:
                ph_dates = ph["photo"]["dates"]
                taken = ph_dates["taken"]
                taken = taken.split(" ")
                ymd = taken[0]
                ymd = ymd.replace("-", "/")

                ph["_prefix"] = dots + ymd

            body = date_template.render(date=d, photos=photos, page=page, pages=len(pages), prev=prev, next=next, dots=dots)

            fname = "page%s.html" % page

            path = os.path.join(dt_root, fname)

            fh = open(path, "w")
            fh.write(body.encode("utf8"))
            fh.close()

            print "wrote %s" % path
            page += 1

        page_one = os.path.join(dt_root, "page1.html")
        index = os.path.join(dt_root, "index.html")

        shutil.copy(page_one, index)

    # 

    photos = {}
    years = []

    for d in dates:

        if len(d.split("-")) != 2:
            continue

        ids = by_date[d]
        count = len(ids)

        dt = datetime.datetime.strptime(d, '%Y-%m')
        m = photos.get(dt.year, [])

        m.append((dt, count))
        photos[dt.year] = m

    years = photos.keys()
    years.sort()

    index_template = env.get_template('index.html')
    body = index_template.render(years=years, photos=photos)

    index_path = os.path.join(source, "index.html")

    fh = open(index_path, "w")
    fh.write(body.encode("utf-8"))
    fh.close()

    #

    css_root = os.path.join(source, "css")

    if not os.path.exists(css_root):
        os.makedirs(css_root)

    css_path = os.path.join(css_root, "index.css")

    css_template = env.get_template('index.css')
    body = css_template.render()

    fh = open(css_path, "w")
    fh.write(body.encode("utf-8"))
    fh.close()

    #

    js_root = os.path.join(source, "js")

    if not os.path.exists(js_root):
        os.makedirs(js_root)

    js_path = os.path.join(js_root, "index.js")

    js_template = env.get_template('index.js')
    body = js_template.render()

    fh = open(js_path, "w")
    fh.write(body.encode("utf-8"))
    fh.close()
