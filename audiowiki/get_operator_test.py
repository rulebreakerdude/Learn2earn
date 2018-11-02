import json
import requests
import datetime
from dblearn2earn import *

z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
number='9717078576'
op_code_map={'1':'AL','28':'AT','8':'IDX','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD'}

op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=9717078576&type=text")
op_code=str(op_code_map[op_info.text.split(",")[0]])
jolo_to_im={'AT':'AR'}
op_code_im=jolo_to_im[op_code]
print op_code_im
rech = requests.post('http://www.imwallet.in/API/APIService.aspx?userid=8527837805&pass=23235&mob=3717078576&opt=%s&amt=10&agentid=%s&optional1=10&fmt=json' %(str(op_code_im),str(z)))
d=(rech.text.split(':')[1]).split(',')[0]
if d=="\"FAILED\"":
	print 'ss'
print d
print rech
print rech.text

