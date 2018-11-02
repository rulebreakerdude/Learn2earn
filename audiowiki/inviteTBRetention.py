#!/usr/bin/env python

import random
import wget
import csv
import os
import shutil
from collections import defaultdict
from dblearn2earn import *
import requests
import json
import subprocess
import urllib3


username="arvindkhadri"
passwd="59849764"
url="http://api.smscountry.com/SMSCwebservice_bulk.aspx"

def sendSMS(number, message):
    data = {'user': username, 'passwd': passwd, 'message': message, 'mobilenumber':number, 'mtype':'N', 'DR':'Y'}
    sms = requests.get(url, params=data, timeout=60)
    if sms.status_code == 200:
        return sms
    else:
        return False


def placeCallFile(number):
    filename = 'main-'+str(number)+'.call'
    f = open('/tmp/'+filename, 'w')
    f.write('Context: callback-learn2earn2\n'+'Extension: 1\n'+"MaxRetries: 1\n"+
            "RetryTime: 30\n"+
            "Channel: dahdi/g1/0"+ str(number) +"\n" +
            "SetVar: swaraChannel="+ 'main' + "\n" +
            "SetVar: targetnumber="+ str(number) +"\n" +
            "callerid: " + str(number) + "\n" +
            "Account: " + str(number) + "\n")
    f.close()
    shutil.move(('/tmp/'+filename), ('/var/spool/asterisk/outgoing/'+filename))

if __name__=='__main__':

    #print "hellow is this working"
    user_details = defaultdict(list)
    # with open('500numbers.csv') as f:
    #     reader = csv.DictReader(f) # read rows into a dictionary format
    #     for row in reader: # read a row as {column1: value1, column2: value2,...}
    #         for (k,v) in row.items(): # go over each column name and value
    #             user_details[k].append(v) # append the value into the appropriate list
    db = Database('learn2earnhindi','greenlantern')
    #db.insertTB100()
    db.insertRetention()
    #list_ph_tb = db.getTb100()
    list_ph_ret = db.getRetention100()
    #placeCallFile(list_ph_tb[0])
    #placeCallFile(list_ph_tb[1])
    placeCallFile(list_ph_ret[0])
    placeCallFile(list_ph_ret[1])
    #s1 = sendSMS(list_ph_tb[0], 'Kamaai Ke Liye Padhaai ki taraf se namaskar! Aapke acche kaam ko dekhkar, TB ke baare mein kuch asaan sawaalon ka jawab dekar das rupay ka top-up jeetne ke liye aapko chuna jata hai. Bhaag lene ke liye kripaya <07714233002> pe call kare.')
    #db.addTBStatus(list_ph_tb[0],s1.status_code, s1.text)
    #s2 = sendSMS(list_ph_tb[1], 'Kamaai Ke Liye Padhaai ki taraf se namaskar! Aapke acche kaam ko dekhkar, TB ke baare mein kuch asaan sawaalon ka jawab dekar das rupay ka top-up jeetne ke liye aapko chuna jata hai. Bhaag lene ke liye kripaya <07714233002> pe call kare.')
    #db.addTBStatus(list_ph_tb[1],s2.status_code, s2.text)
    s3 = sendSMS(list_ph_ret[0], 'Kamaai Ke Liye Padhaai  ki taraf se namaskar! Aapke acche kaam ko dekhkar, Kuch asan sawal ka jawab dekar das rupay ka top-up jeetne ke liye aapko chuna jata hai. Baag lene keliye krupaya <07714233002> pe call kare.')
    db.addRetStatus(list_ph_ret[0],s3.status_code, s3.text)
    s4 = sendSMS(list_ph_ret[1], 'Kamaai Ke Liye Padhaai  ki taraf se namaskar! Aapke acche kaam ko dekhkar, Kuch asan sawal ka jawab dekar das rupay ka top-up jeetne ke liye aapko chuna jata hai. Baag lene keliye krupaya <07714233002> pe call kare.')
    db.addRetStatus(list_ph_ret[1],s4.status_code, s4.text)
    #print calling_number_tb_1
    f = open('calling.log', 'ab')
    #f.write("Calling phone number:"+str(list_ph_tb[0])+"\n")
    #f.write("Calling phone number:"+str(list_ph_tb[1])+"\n")
    f.write("Calling phone number:"+str(list_ph_ret[0])+"\n")
    f.write("Calling phone number:"+str(list_ph_ret[1])+"\n")
    f.close()
    #      #a.writerow(calling_number_ret_1)
         #a.writerow(calling_number_ret_2)

    #print  list_ph
    print "inserted"
