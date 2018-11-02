import json
import requests
import datetime
from dblearn2earn import *

z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
db = Database('learn2earnhindi','root')
db.addHivSessionID("t1",1,z)
si=db.isHivRechargedSuccess(7767919121)
print si
si=si+1
print si
db.addHivSessionID("t2",str(si),si)
