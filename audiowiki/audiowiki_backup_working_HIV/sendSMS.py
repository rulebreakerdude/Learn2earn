#-*- coding: utf-8 -*-
import requests
import smsConf as conf

def sendSMS(number, message):
    data = {'user': conf.username, 'passwd': conf.passwd, 'message': message, 'mobilenumber':number, 'mtype':'OL', 'DR':'Y'}
    sms = requests.get(conf.url, params=data, timeout=60)
    if sms.status_code == 200:
        return sms
    else:
        return False

def notifyOnPublish(number):
    data = {'user': conf.username, 'passwd': conf.passwd, 'message': conf.notifySms, 'mobilenumber': number, 'mtype': 'OL', 'DR': 'Y'}
    sms = requests.get(conf.url, params=data, timeout=60)
    if sms.status_code == 200:
        return sms.text
    return False

#s = sendSMS('9819241289', '0928092E0938094D0924094700200906092A0915093E002009380928094D09260947093600200905092C002009380940091C094009280947091F0020092A093000200909092A094D0932092C094D09270020093909480964');
#s = notifyOnPublish('9819241289')
#print 'Got', s
#if s:
#    print s.status_code, s.text	
