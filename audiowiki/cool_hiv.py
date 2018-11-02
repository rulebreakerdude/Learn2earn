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
number='0'
global q_to_ask
q_to_ask=[1,2,3,4,5,6]
global points
points=0
ref_dic_loc= '/home/swara/referral_data/rd_hiv.json'#File to store referral data
rec_dic_loc= '/home/swara/referral_data/recharge_status_hiv.json'#File to store recharge data
JOLO_API=326208132556249

#jolo specific operator code map
op_code_map={'1':'AL','28':'AT','3':'BS','8':'IDX','29':'JO','20':'MTD','6':'MTM','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD'}

sys.setrecursionlimit(15000)

##### State functions ######

def login_hiv():
    keyDict = newKeyDict()
    keyDict['1'] = (consent_info,())
    keyDict['9'] = (equal_prob,())
    playFile(PROMPTS_DIR+'HIV/Intro',keyDict)



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
        playFile(PROMPTS_DIR+'HIV/Awareness_scenario',keyDict)
    else:
        playFile(PROMPTS_DIR+'HIV/Treatment_scenario',keyDict)  



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
    playFile(PROMPTS_DIR+'HIV/Consent_Info',keyDict)


    
def intro_questions():
    keyDict = newKeyDict()
    keyDict['1'] = (intro_questions,())
    keyDict['2'] = (random_ques,())
    keyDict['3'] = (intro_questions,())
    keyDict['4'] = (intro_questions,())
    keyDict['5'] = (intro_questions,())
    keyDict['6'] = (intro_questions,())
    keyDict['7'] = (intro_questions,())
    keyDict['8'] = (intro_questions,())
    keyDict['9'] = (intro_questions,())
    playFile(PROMPTS_DIR+'HIV/Intro_questions',keyDict)

    
    
def random_ques():
    random.shuffle(q_to_ask,random.random)
    debugPrint('First question will be q'+str(q_to_ask[0]))
    switcher={1:q1,2:q2,3:q3,4:q4,5:q5,6:q6}   
    switcher[q_to_ask[0]](0)
    switcher[q_to_ask[1]](1)
    switcher[q_to_ask[2]](2)
    switcher[q_to_ask[3]](3)
    switcher[q_to_ask[4]](4)
    switcher[q_to_ask[5]](5)
    recharge_new()
    
    
    
def q1(q_answered):
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,())
    keyDict['2'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q1',keyDict)
    
def q2(q_answered):
    keyDict = newKeyDict()
    keyDict['2'] = (increase_points,())
    keyDict['1'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q2',keyDict)
    
def q3(q_answered):
    keyDict = newKeyDict()
    keyDict['2'] = (increase_points,())
    keyDict['1'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q3',keyDict)
    
def q4(q_answered):
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,())
    keyDict['2'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q4',keyDict)
    
def q5(q_answered):
    keyDict = newKeyDict()
    keyDict['1'] = (increase_points,())
    keyDict['2'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q5',keyDict)
    
def q6(q_answered):
    keyDict = newKeyDict()
    keyDict['3'] = (increase_points,())
    keyDict['1'] = (do_nothing,())
    keyDict['2'] = (do_nothing,())
    playFile(PROMPTS_DIR+'HIV/Q6',keyDict)
 
def increase_points():
    global points
    debugPrint('New points are '+str(points))
    points=points+1

def do_nothing():
    debugPrint('doing nothing') 
    
def recharge_new():
    global points
    global tendigit
    global number
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
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/enter_friend_number')
    while (tendigit > 0):
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict) 
    if (tendigit == 0):
        debugPrint('The final points are ' + str(points)+' against the number '+str(number))
        recData={}
        with open(rec_dic_loc,'r') as recFile:
            recData=json.load(recFile)
        recFile.close()
        if number not in recData:
            recData[str(number)]=[points,0,0]
            op_info=requests.get("https://joloapi.com/api/findoperator.php?userid=devansh76&key=326208132556249&mob=%s&type=text" %(str(number[1:])))
            op_code=str(op_code_map[op_info.text.split(",")[0]])
            debugPrint('Got the operator Code as '+op_code)
            z='{:%Y%m%d%H%M%S}'.format(datetime.datetime.now())
            if points == 6:
                rech=requests.get("https://joloapi.com/api/recharge.php?mode=0&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=20&orderid=%s&type=text" % (op_code,str(number)[1:],z))
            elif points>=3:
                rech=requests.get("https://joloapi.com/api/recharge.php?mode=0&userid=devansh76&key=326208132556249&operator=%s&service=%s&amount=10&orderid=%s&type=text" % (op_code,str(number)[1:],z))
            debugPrint(str(rech.text))
        else:
            debugPrint('Chacha already here')
        recFileW=open(rec_dic_loc,'w')
        json.dump(recData,recFileW,indent=4)
        recFileW.close()
        hangup()

def recordNumber(key):
         global tendigit
         global number
         if ((int(key) == 0) and (int(number) > 0)) or (int(key) > 0):
             number+=key
             tendigit-=1
             debugPrint(number)
             debugPrint(str(tendigit))
             if tendigit == 0:
                signal.signal(signal.SIGHUP, signal.SIG_IGN)
                signal.signal(signal.SIGHUP, signal.SIG_DFL)    

if __name__=='__main__':
    # Read and ignore AGI environment (read until blank line)
    log_file = open('/home/swara/audiowiki/web/out.txt', 'w')
    log_file.write("test begins the program")
    log_file.flush()
    log_file.close()
    env = {}
    tests = 0;
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
    while True:
        try:
            login_hiv()
        except KeyPressException, e:
            if e.key != '0':
                #db.addInvalidkeyEvent(e.key, 'mm', 5) Arjun patched with CallID
                db.addInvalidkeyEvent(e.key, 'mm', 5, callID)
            else:
                continue
    hangup()
    