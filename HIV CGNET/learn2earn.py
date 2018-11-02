#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import smtplib
import sys
import os
import signal
import re
import time
import requests
import json
import random
from random import randint
import copy
from utilities import *
from asteriskinterface import *
from dblearn2earn import *
import datetime

language = 'kannada' # Default language is kannada
SOUND_DIR = '/var/lib/asterisk/sounds/audiowikiIndia/'
PROMPTS_DIR = SOUND_DIR + 'prompts/' # extended during setup (the main procedure adds the "main/" after the PROMPTS_DIR path)
AST_SOUND_DIR = '/var/lib/asterisk/sounds/'
tendigit = 10
fivedigit = 5
number='0'
global user
global entered_code
entered_code=''
user='0'
global q_to_ask
global flag
flag=0
q_to_ask=[1,2,3,4,5,6]
global ans_received
ans_received=[0,0,0,0,0,0]
global points
global question
points=0
lfl='/home/swara/audiowiki/hiv/referral_data/log_file.json'

#jolo specific operator code map
op_code_map={'1':'AL','28':'AT','8':'IDX','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD','22':'VF'}
fail_map={'0':'JO','29':'JO','20':'MTD','6':'MTM','3':'BS'}
sys.setrecursionlimit(15000)

def login_hiv():
    keyDict = newKeyDict()
    keyDict['2'] = (hangup,())
    keyDict['1'] = (expln,())
    playFile(PROMPTS_DIR+'HIV/intro',keyDict)
    expln()

def expln():
    keyDict = newKeyDict()
    keyDict['1'] = (intro_questions,())
    playFile(PROMPTS_DIR+'HIV/expln',keyDict)
    intro_questions()

def consent_info():
    keyDict = newKeyDict()
    keyDict['1'] = (equal_prob,())
    keyDict['2'] = (equal_prob,())
    keyDict['3'] = (equal_prob,())
    keyDict['4'] = (equal_prob,())
    keyDict['5'] = (equal_prob,())
    keyDict['6'] = (equal_prob,())
    keyDict['7'] = (equal_prob,())
    keyDict['8'] = (equal_prob,())
    keyDict['9'] = (equal_prob,())
    playFile(PROMPTS_DIR+'HIV/consent_info',keyDict)
    intro_questions()

def equal_prob():
    #dum module because asterisk does not support waterfalls
    keyDict = newKeyDict()
    keyDict['1'] = (intro_questions,())
    keyDict['2'] = (intro_questions,())
    keyDict['3'] = (intro_questions,())
    keyDict['4'] = (intro_questions,())
    keyDict['5'] = (intro_questions,())
    keyDict['6'] = (intro_questions,())
    keyDict['7'] = (intro_questions,())
    keyDict['8'] = (intro_questions,())
    keyDict['9'] = (intro_questions,())
    a=randint(1,2)
    if a==1:
        playFile(PROMPTS_DIR+'HIV/awareness_scenario',keyDict)
    else:
        playFile(PROMPTS_DIR+'HIV/treatment_scenario',keyDict)
    intro_questions()

def intro_questions():
    keyDict = newKeyDict()
    keyDict['1'] = (random_ques,())
    keyDict['2'] = (random_ques,())
    keyDict['3'] = (random_ques,())
    keyDict['4'] = (random_ques,())
    keyDict['5'] = (random_ques,())
    keyDict['6'] = (random_ques,())
    keyDict['7'] = (random_ques,())
    keyDict['8'] = (random_ques,())
    keyDict['9'] = (random_ques,())
    playFile(PROMPTS_DIR+'HIV/intro_questions',keyDict)
    random_ques()

def random_ques():
    random.shuffle(q_to_ask,random.random)
    debugPrint('First question will be q'+str(q_to_ask[0]))
    switcher={1:q1,2:q2,3:q3,4:q4,5:q5,6:q6}
    playFile(PROMPTS_DIR+'HIV/_Q1')
    switcher[q_to_ask[0]]()
    playFile(PROMPTS_DIR+'HIV/_Q2')
    switcher[q_to_ask[1]]()
    playFile(PROMPTS_DIR+'HIV/_Q3')
    switcher[q_to_ask[2]]()
    playFile(PROMPTS_DIR+'HIV/_Q4')
    switcher[q_to_ask[3]]()
    playFile(PROMPTS_DIR+'HIV/_Q5')
    switcher[q_to_ask[4]]()
    playFile(PROMPTS_DIR+'HIV/_Q6')
    switcher[q_to_ask[5]]()
    for i in range(0,2):
        if ans_received[0]!='2':
            i=0
            q1()
        if ans_received[1]!='1':
            i=0
            q2()
        if ans_received[2]!='2':
            i=0
            q3()
        if ans_received[3]!='2':
            i=0
            q4()
        if ans_received[4]!='1':
            i=0
            q5()
        if ans_received[5]!='1':
            i=0
            q6()
    playFile(PROMPTS_DIR+'HIV/quizend')
    tell_points()

def q1():
    keyDict = newKeyDict()
    keyDict['1'] = (tell_correct_ans,('q1','1'))
    keyDict['2'] = (increase_points,('q1','2'))
    keyDict['3'] = (q1,())
    playFile(PROMPTS_DIR+'HIV/Q1',keyDict)

def q2():
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,('q2','1'))
    keyDict['2'] = (tell_correct_ans,('q2','2'))
    keyDict['3'] = (q2,())
    playFile(PROMPTS_DIR+'HIV/Q2',keyDict)

def q3():
    keyDict = newKeyDict()
    keyDict['2'] = (increase_points,('q3','2'))
    keyDict['1'] = (tell_correct_ans,('q3','1'))
    keyDict['3'] = (q3,())
    playFile(PROMPTS_DIR+'HIV/Q3',keyDict)

def q4():
    keyDict = newKeyDict()
    keyDict['2'] = (increase_points,('q4','2'))
    keyDict['1'] = (tell_correct_ans,('q4','1'))
    keyDict['3'] = (q4,())
    playFile(PROMPTS_DIR+'HIV/Q4',keyDict)

def q5():
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,('q5','1'))
    keyDict['2'] = (tell_correct_ans,('q5','2'))
    keyDict['3'] = (q5,())
    playFile(PROMPTS_DIR+'HIV/Q5',keyDict)
 
def q6():
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,('q6','1'))
    keyDict['3'] = (q6,())
    keyDict['2'] = (tell_correct_ans,('q6','2'))
    playFile(PROMPTS_DIR+'HIV/Q6',keyDict)

def tell_correct_ans(question,response):
    global user
    global flag
    flag=1
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    db.addHivResponse(user,question,response,z)
    if question=='q1':
        ans_received[0]=response
        playFile(PROMPTS_DIR+'HIV/-Q1')
    if question=='q2':
        ans_received[1]=response
        playFile(PROMPTS_DIR+'HIV/-Q2')
    if question=='q3':
        ans_received[2]=response
        playFile(PROMPTS_DIR+'HIV/-Q3')
    if question=='q4':
        ans_received[3]=response
        playFile(PROMPTS_DIR+'HIV/-Q4')
    if question=='q5':
        ans_received[4]=response
        playFile(PROMPTS_DIR+'HIV/-Q5')
    if question=='q6':
        ans_received[5]=response
        playFile(PROMPTS_DIR+'HIV/-Q6')

def increase_points(question,response):
    global points
    global user
    debugPrint('New points are '+str(points))
    points=points+1
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    db.addHivResponse(user,question,response,z)
    if question=='q1':
        ans_received[0]=response
    if question=='q2':
        ans_received[1]=response
    if question=='q3':
        ans_received[2]=response
    if question=='q4':
        ans_received[3]=response
    if question=='q5':
        ans_received[4]=response
    if question=='q6':
        ans_received[5]=response

def do_nothing(question,response):
    global user
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    db.addHivResponse(user,question,response,z)

def tell_points():
    global points
    global user
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    db.addHivPoints(user,points,z)
    if points==1:
        playFile(PROMPTS_DIR+'HIV/1of6')
    if points==2:
        playFile(PROMPTS_DIR+'HIV/2of6')
    if points==3:
        playFile(PROMPTS_DIR+'HIV/3of6')
    if points==4:
        playFile(PROMPTS_DIR+'HIV/4of6')
    if points==5:
        playFile(PROMPTS_DIR+'HIV/5of6')
    if points==6:
        playFile(PROMPTS_DIR+'HIV/6of6')
    playFile(PROMPTS_DIR+'HIV/more_info')
    permission()

def permission():
    global user
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    keyDict = newKeyDict()
    keyDict['1'] = (db.addHivResponse,(user,'permissionToCall','yes',z))
    keyDict['2'] = (db.addHivResponse,(user,'permissionToCall','no',z))
    playFile(PROMPTS_DIR+'HIV/permission',keyDict)
    enter_referral()
      
def code():
    global user
    #playFile(PROMPTS_DIR+'HIV/code')
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    referral=user[-5:]
    if db.doesUserHaveReferral(user):
        #play_referral(db.referralAgainstUser(user))
        z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    else:
        while(db.isHivReferral(referral)):
            referral=str(int(referral)+1)
        db.addHivReferral(user,referral,z)
        #play_referral(referral)
    enter_referral()
        
def play_referral(referral):
    for i in referral:
        loc=PROMPTS_DIR+'HIV/'+str(i)
        playFile(loc)
    enter_referral()
    
def enter_referral():
    global user
    keyDict = newKeyDict()
    keyDict['1'] = (enter_code,())
    keyDict['3'] = (code,())
    keyDict['2'] = (recharge_new,(user,points,'quiztaker'))
    playFile(PROMPTS_DIR+'HIV/enter_referral', keyDict)
    hangup()
    
def enter_code():
    global points
    global fivedigit
    global entered_code
    entered_code=''
    global user
    fivedigit=5
    keyDict = newKeyDict()
    keyDict['0'] = (recordNumber,('0',))
    keyDict['1'] = (recordNumber,('1',))
    keyDict['2'] = (recordNumber,('2',))
    keyDict['3'] = (recordNumber,('3',))
    keyDict['4'] = (recordNumber,('4',))
    keyDict['5'] = (recordNumber,('5',))
    keyDict['6'] = (recordNumber,('6',))
    keyDict['7'] = (recordNumber,('7',))
    keyDict['8'] = (recordNumber,('8',))
    keyDict['9'] = (recordNumber,('9',))
    playFile(PROMPTS_DIR+'HIV/enter_code', keyDict)
    while(fivedigit > 0):
        playFile(PROMPTS_DIR+'HIV/empty_pause', keyDict)
    if (fivedigit == 0 and (db.userAgainstReferral(entered_code))[-10:] != user):
        z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        db.addHivResponse(user,'enter referral',entered_code,z)
        recharge_new(user,points,'quiztaker')
        recharge_new((db.userAgainstReferral(entered_code))[-10:],points,'referred')
        if not db.isHivPair(user,(db.userAgainstReferral(entered_code))[-10:]):
            db.addHivPair(user,(db.userAgainstReferral(entered_code))[-10:],z)
    hangup()

def recharge_new(number,points,who):
    global user
    global flag
    if user=='9717078576' or user=='8527837805' or number == '9717078576' or (who=='quiztaker' and db.isHivRechargedSuccess(number)==False) or (who=='referred' and not db.isHivAlreadyReferred(user)):
        z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
        if db.isHivRechargedSuccess(number):
            op_code=db.operatorAgainstUser(number)
        else:
            op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=%s&type=text" %(str(number)))
            if op_info.text.split(",")[0] in op_code_map:
                op_code=str(op_code_map[op_info.text.split(",")[0]])
                cir_code=str(op_info.text.split(",")[1])
            elif op_info.text.split(",")[0] in fail_map:
                return 0
            else:
                op_code="AT"# defaulting to airtel
        z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())     
        if flag==0 and who=='quiztaker':
            amount='20'
        else:
            amount='10'
        

        if points>=3:
            rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (op_code,str(number),amount,z))
            db.addHivRechargeStatus(str(number),str(rech.text),z)
            #functionality specific to addressing JOLO errors
            if rech.text.split(',')[0]=='FAILED':
                MNP_issue(number,amount,op_code)
            else:
                db.addHivRechargeSuccessStatus(str(number),str(op_code),str(rech.text),z)

    else:
        debugPrint('Chacha already here')

def MNP_issue(number,amount,op_code):
    op_list=['TW','T24S','T24','VC','VGS','VG','VDS','VD','TI','TDS','TD','AL','MS','UNS','UN','RG','RL','VF','IDX','BSS','BS','AT']
    z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
    for i in op_list:
        rech=requests.get("https://joloapi.com/api/recharge.php?mode=1&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=%s&orderid=%s&type=text" % (str(i),number,amount,z))
        if rech.text.split(',')[0] != 'FAILED':
            break
    db.addHivRechargeStatus(str(number),str(rech.text),z)
    if rech.text.split(',')[0]!='FAILED':
        db.addHivRechargeSuccessStatus(str(number),str(i),str(rech.text),z)
    else:
        recharge_imwallet(number,amount,op_code)
                
def recharge_imwallet(number,amount,op_code):
    jolo_to_im={'AT':'AR','IDX':'ID','VF':'VF','AL':'AC','MTS':'M','RL':'RC','RG':'RG','UN':'UN','VD':'VC'}
    op_code_im=jolo_to_im[op_code]
    rech = requests.post('http://www.imwallet.in/API/APIService.aspx?userid=8527837805&pass=23235&mob=%s&opt=%s&amt=%s&agentid=%s&optional1=10&fmt=json' %(str(number),str(op_code_im),str(amount),str(z)))
    p=(rech.text.split(':')[1]).split(',')[0]
    db.addHivRechargeStatus(str(number),str(p),z)
    if p!="\"FAILED\"":
        db.addHivRechargeSuccessStatus(str(number),str(op_code),str(rech.text),z)
    

def recordNumber(key):
    global fivedigit
    global entered_code
    if fivedigit > 0:
        entered_code+=key
        fivedigit-=1
                

if __name__=='__main__':
    global user
    # Read and ignore AGIfile environment (read until blank line)
    env = {}
    while True:
        line = sys.stdin.readline().strip()
        sys.stderr.write(line)
        sys.stderr.flush()
        if line == '':
            break
        key,data = line.split(':')
        if key[:4] != 'agi_':
            #skip input that doesn't begin with agi_
            sys.stderr.write("Did not work!\n")
            sys.stderr.flush()
            continue
        key = key.strip()
        data = data.strip()
        if key != '':
            env[key] = data
    sys.stderr.write("AGI Environment Dump:\n")
    sys.stderr.flush()
    for key in env.keys():
        sys.stderr.write(" -- %s = %s\n" % (key, env[key]))
        sys.stderr.flush()
    db = Database('learn2earnhindi','root')
    user = env['agi_callerid']
    # if user isn't detected by callerid, get it from the argument list
    if (user == "unknown" or user == "100"):
        user = env['agi_arg_2']
    # arguments passed from extensions.conf go here!
    swaraChannel = env['agi_arg_1']
    if (swaraChannel == ""):
        swaraChannel = "main"
    PROMPTS_DIR = PROMPTS_DIR + swaraChannel + "/"
    # arvind's code to count keypresses throwing error on early exit
    #signal.signal(signal.SIGHUP, checkCaller)
    user=str(user[-10:])
    login_hiv()
    while True:
        try:
            pass
        except KeyPressException, e:
            if e.key != '0':
                #db.addInvalidkeyEvent(e.key, 'mm', 5) Arjun patched with CallID
                db.addInvalidkeyEvent(e.key, 'mm', 5, callID)
            else:
                continue
    hangup()
