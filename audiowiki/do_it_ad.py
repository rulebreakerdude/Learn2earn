from dblearn2earn import *
import datetime
import requests

z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
print z
op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=9421273856&type=text")
print op_info.text
rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=AT&service=9717078576&amount=10&orderid=%s&type=text" % (z))
print rech.text