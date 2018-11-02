import requests
import json
import datetime
import string

def MNP_issue(number,amount):
	op_list=['TW','T24S','T24','VC','VGS','VG','VDS','VD','MTMS','MTM','MTDS','MTD','TI','TDS','TD','AL','MS','UNS','UN','RG','RL','VF','JO','IDX','BSS','BS','AT']
	op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=9146749329&type=text")
	print op_info.text
	op_code=op_info.text.split(',')[0]
	circle_code=op_info.text.split(',')[1]
	z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
	print op_code
	f='/home/swara/audiowiki/hiv/MNP_test.json'
	with open(f,'r') as o:
		b=json.load(o)
	o.close()
	if b[j].split(',')[0]=='FAILED':
		for i in op_list:
			rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(i),j[1:],amount,z))
			if rech.text.split(',')[0] != 'FAILED':
				d[j+i]=rech.text
				break
	with open(f,'w') as recFailFile:
		json.dump(d,recFailFile,indent=4)
	recFailFile.close()	