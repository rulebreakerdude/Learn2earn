#!/usr/bin/python
# -*- coding: utf-8 -*-
#Menu system
import smtplib
import sys
import stopwatch
import os
import signal
import re
import time
import requests
import json
import random
from random import randint
import copy
import sendSMS
from utilities import *
from asteriskinterface import *
from dblearn2earn import *
from mutagen.mp3 import MP3

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
REF_DIC_LOC= '/home/swara/referral_data/rd_hiv.json'#File to store referral data

sys.setrecursionlimit(15000)
Circles = {'Haryana': '7', 'Punjab': '18', 'Kerala': '11', 'Madhya Pradesh Chhattisgarh': '14', 'UP West': '22', 'Kolkata': '12', 'Orissa': '17', 'Tamil Nadu': '20', 'Chennai': '4', 'Mumbai': '15', 'Assam': '2', 'West Bengal': '23', 'Rajasthan': '19', 'North East': '16', 'Andhra Pradesh': '1', 'Jammu Kashmir': '9', 'Himachal Pradesh': '8', 'Gujarat': '6', 'Maharashtra': '13', 'UP East': '21', 'Delhi NCR': '5', 'Karnataka': '10', 'Bihar Jharkhand': '3'}
Operators = {'BSNL': '3', 'VIRGIN GSM': '14', 'MTS': '13', 'VIRGIN CDMA': '12', 'TATA DOCOMO GSM': '11', 'MTNL': '25', 'IDEA': '8', 'RELIANCE GSM': '5', 'TATA INDICOM': '9', 'AIRTEL': '1', 'LOOP MOBILE': '10', 'UNINOR': '16', 'AIRCEL': '6', 'RELIANCE CDMA': '4', 'VIDEOCON': '17', 'VODAFONE': '2'}


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
    debugPrint(str(q_to_ask[0]))
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
    debugPrint('points are '+str(points))
    points=points+1

def do_nothing():
    debugPrint('doing nothing') 
	
def recharge_new():
    global points
    global tendigit
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
    debugPrint('it usually doesnt flow here')
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/enter_friend_number')
    #recordEvent('Timer','0','playedEnterFriendNumber','',enterNumber)
    debugPrint('it usually doesnt flow here')
    while (tendigit > 0):
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
          
    if (tendigit == 0):
        debugPrint('The final points are' + str(points))
    hangup()

def recordNumber(key):
         global tendigit
         global number
         debugPrint("i am here in record")
         if ((int(key) == 0) and (int(number) > 0)) or (int(key) > 0):
             debugPrint("i am here in inside counter check")
             number+=key
             tendigit-=1
             debugPrint(number)
             debugPrint(str(tendigit))
             if tendigit == 0:
                signal.signal(signal.SIGHUP, signal.SIG_IGN)
                debugPrint('Phew di Pie')
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
    