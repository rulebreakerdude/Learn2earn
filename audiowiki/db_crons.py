from dblearn2earn import *
import datetime
import requests


def MNP_issue(number,amount):
	op_code_map={'0':'JO','1':'AL','28':'AT','3':'BS','8':'IDX','29':'JO','20':'MTD','6':'MTM','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD'}
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=%s&type=text" %(str(number)))
	if op_info.text.split(",")[0] in op_code_map:
		op_code=str(op_code_map[op_info.text.split(",")[0]])
	else:
		op_code="UN"
	rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(op_code),number,amount,z))
	if rech.text.split(',')[0] == 'FAILED':
		op_list=['TW','T24S','T24','VC','VGS','VG','VDS','VD','TI','TDS','TD','AL','MS','UNS','UN','RG','RL','VF','IDX','BSS','BS','AT']
		for i in op_list:
			rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(i),number,amount,z))
			if rech.text.split(',')[0] != 'FAILED':
				break
		if rech.text.split(',')[0]!='FAILED':
			db.addHivRechargeSuccessStatus(str(number),str(i),str(rech.text),z)
			db.addHivRechargeRider(str(number),str(i),str(rech.text),z)
		else:
			db.addHivRechargeStatus(str(number),str(rech.text),z)
	else:
		db.addHivRechargeSuccessStatus(str(number),str(op_code),str(rech.text),z)
		db.addHivRechargeRider(str(number),str(op_code),str(rech.text),z)
op_code_map={'0':'JO','1':'AL','28':'AT','3':'BS','8':'IDX','29':'JO','20':'MTD','6':'MTM','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD'}
db = Database('learn2earnhindi','root')
now = datetime.datetime.now()
now_minus_10 = now - datetime.timedelta(minutes = 4)
job_time='{:%Y%m%d%H%M%S}'.format(now)
from_time='{:%Y%m%d%H%M%S}'.format(now_minus_10)	
a=db.getFailedRecharges(from_time,job_time)
b=db.getSuccessfulRecharges(from_time,job_time)

c=[]
for item in a:
	if item not in b:
		c.append(item)
		print (item)
for number in c:
	MNP_issue(number,10)

x='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
db.addCronLog(x)