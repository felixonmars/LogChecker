#!/usr/bin/env python2
import urllib, urllib2, re
s = urllib2.urlopen("http://www.accuraterip.com/driveoffsets.htm").read().replace("\n", "").replace("\r", "")

from pymongo import Connection
mongo = Connection('127.0.0.1', 27017, safe = True)
db = mongo.logchecker
db.authenticate('felix', '')
db.offset.drop()

for t in [re.sub(r"\$+", "$", re.sub(r"<[^>]+>", "$", x)).strip("$").split("$") for x in s.split("</tr>")[1:-2]]:
    try:
        name, offset, submit, accu = t
        name = re.sub(r"\s+", " ", name)
        name = name.strip()
        keywords = name.split()
    except:
        print "*** ERROR ", t
    db.offset.insert(dict(name = name, offset = offset, keywords = keywords))

db.offset.ensure_index("keywords")
