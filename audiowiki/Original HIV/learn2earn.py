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
PROMPTS_DIR = SOUND_DIR + 'prompts/' # extended during setup
AST_SOUND_DIR = '/var/lib/asterisk/sounds/'
tendigit = 10
number='0'

"""
sharma64: Location for directory containing the referral lookup dictionary
"""
REF_DIC_LOC= '/home/swara/referral_data/rd.json'
"""
sharma64: Fork End
"""
sys.setrecursionlimit(15000)
Circles = {'Haryana': '7', 'Punjab': '18', 'Kerala': '11', 'Madhya Pradesh Chhattisgarh': '14', 'UP West': '22', 'Kolkata': '12', 'Orissa': '17', 'Tamil Nadu': '20', 'Chennai': '4', 'Mumbai': '15', 'Assam': '2', 'West Bengal': '23', 'Rajasthan': '19', 'North East': '16', 'Andhra Pradesh': '1', 'Jammu Kashmir': '9', 'Himachal Pradesh': '8', 'Gujarat': '6', 'Maharashtra': '13', 'UP East': '21', 'Delhi NCR': '5', 'Karnataka': '10', 'Bihar Jharkhand': '3'}
Operators = {'BSNL': '3', 'VIRGIN GSM': '14', 'MTS': '13', 'VIRGIN CDMA': '12', 'TATA DOCOMO GSM': '11', 'MTNL': '25', 'IDEA': '8', 'RELIANCE GSM': '5', 'TATA INDICOM': '9', 'AIRTEL': '1', 'LOOP MOBILE': '10', 'UNINOR': '16', 'AIRCEL': '6', 'RELIANCE CDMA': '4', 'VIDEOCON': '17', 'VODAFONE': '2'}


##### State functions ######

def login():
    """
    Login: If the user's phone number (var 'user') is unrecognized,
    the system stores it in the "user" table.

    Audio Files:
    """

    

    global callID
    callID=db.newCall(user)
    debugPrint("detected caller id is="+user)

    """
    sharma64: Creating referral code when first time user
    """
    refData={}
    refFile=open(REF_DIC_LOC,'r')
    refData=json.load(refFile)
    refFile.close()
    refFileW=open(REF_DIC_LOC,'w')
    debugPrint('File loaded. Trying user form view now')
    debugPrint('See the format '+user)
 	
    if user not in refData:
        refCode=(str(user))[-5:]
        while refCode in refData:
            refCode=str((int(refCode)+1)%100000)
        refData[refCode]=str(user)
        refData[str(user)]=refCode

    json.dump(refData,refFileW,indent=4)


    debugPrint('User Added with code')
    """
    sharma64: Fork End
    """

    if not db.isUser(user): # If the phone number calling the system is
                            # unrecognized by the database, add the number
                            # as a new user to table 'users'.
        db.addUser(user)
        newUserMessage = str(user) + " ADDED TO DATABASE"
        db.logUserTime(user)
        debugPrint(newUserMessage) # Print message to Asterisk console. NOTE: You must run
                                   # the agi-debug command at console before debug messages
                                   # will appear.


    elif db.isCompletedUser(user):
        db.logUserTime(user)
        completeUser = stopwatch.Timer()
        keyDict = newKeyDict()
        #keyDict['1'] = (playSurvey,())
        keyDict['2'] = (playEnterNumber,())
        debugPrint("this is completed user")
        recordEvent('Timer','0','returnCompletedUser','',completeUser)

        if db.isTB(user) and (not(db.isTBCompleted(user))):
             recordEvent('Timer','0','enteringTBCheck','',completeUser)
             playFile(PROMPTS_DIR+'learn2earn/HindiRaw/welcome')
             recordEvent('Timer','0','playedWelcome','',completeUser)
             playTB()
        elif db.isRetention(user) and (not db.isRetentionCompleted(user)):
             recordEvent('Timer','0','enteringRetentionquiz','',completeUser)
             playFile(PROMPTS_DIR+'learn2earn/HindiRaw/welcome')
             playFile(PROMPTS_DIR+'learn2earn/HindiRaw/retention_intro_new')
             recordEvent('Timer','0','playedWelcome','',completeUser)
             question1(1,True)

        if db.isSurveyCompleted(user):
            debugPrint(str(db.isSurveyCompleted(user)))
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/referrer_end_message')
            #playEnterNumber(True)
            hangup()

        else:
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/referrer_end_message')
            hangup()
            #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/wait_reentry_option',keyDict)
            #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/entry_other_winning_options',keyDict)
            #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/wait_reentry_option',keyDict)
        #<missed option logic>
        #playEnterNumber()

    elif db.isUser(user):
         failedUser = stopwatch.Timer()
         # keyDict = newKeyDict()
         # keyDict['1'] = (mainMenu,())
         # keyDict['2'] = (playEnterNumber,(False))
         # playFile(PROMPTS_DIR+'learn2earn/HindiRaw/coming_back_again',keyDict)
         # playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
         # playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
         recordEvent('Timer','0','returnFailedUser','',failedUser)
         returningUserMessage = "RETURNING USER " + str(user)
         db.logUserTime(user)
         debugPrint(returningUserMessage)

# def myhangup():
#     pid = os.getpid()
#     with open('hungup_pid.csv', 'ab') as csvfile:
#         a = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
#         data = [pid,'hungup']
#         a.writerow(data)
#     hangup()

def playTB():
    TbUser = stopwatch.Timer()
    keyDict = newKeyDict()
    keyDict['1'] = (evaluateTB,('1'))
    keyDict['2'] = (evaluateTB,('2'))
    keyDict['3'] = (evaluateTB,('3'))
    keyDict['4'] = (evaluateTB,('4'))
    keyDict['5'] = (playTB,())
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/TB_welcome_intro')
    recordEvent('Timer','0','Played_TB_intro','',TbUser)
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/TB_ad')
    recordEvent('Timer','0','Played_TB_ad','',TbUser)
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/TB_question', keyDict)
    recordEvent('Timer','0','Played_TB_question','',TbUser)
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
    hangup()
    #logic to tb question into, uestion answer
    #later also check if user has been recharged, he can take it multiple times without money

def evaluateTB(key):
    evaluateTB = stopwatch.Timer()
    db.addTBResponse(user,key)
    if key=='2':
       playFile(PROMPTS_DIR+'learn2earn/HindiRaw/tb_right_answer')
       recharge(user)
       recordEvent('Timer','0','recharged_user','',evaluateTB)
       hangup()
    else:
       playFile(PROMPTS_DIR+'learn2earn/HindiRaw/tb_try_again')
       recordEvent('Timer','0','Played_try_again','',evaluateTB)
       hangup()

def playSurvey():
    surveyTimer = stopwatch.Timer()
    class ageScope:
        ageDigits = 2
        age = '0'
    def surveyQ1(key,repeat):
        surveyPoints=0
        keyDict = newKeyDict()
        q1 = stopwatch.Timer()
        keyDict['1'] = (surveyQ2,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ2,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ2,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ2,('4',True,surveyPoints))
        recordEvent('Timer',key,'surveyQ1','',q1)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question1_edit', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ2('0',False,surveyPoints)

    def recordAge(key):
        recordKey = stopwatch.Timer()
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/keypress')
        recordEvent('Timer',key,'enterAgeNumber','',recordKey)
        if ((int(key) == 0) and (int(ageScope.age) > 0)) or (int(key) > 0):
            debugPrint("i am here in inside counter check")
            ageScope.age+=key
            ageScope.ageDigits-=1

    def surveyQ2(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q2 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q1',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q1',key,surveyPoints)
        keyDict['1'] = (surveyQ3,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ3,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ2,('3',False,surveyPoints))
        recordEvent('Timer',key,'surveyQ2','',q2)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question2', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ3('0',False,surveyPoints)

    def surveyQ3(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q3 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q2',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q2',key,surveyPoints)
        keyDict['1'] = (surveyQ4,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ4,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ3,('3',False,surveyPoints))
        recordEvent('Timer',key,'surveyQ3','',q3)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question3', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ4('0',False,surveyPoints)

    def surveyQ4(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q4 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q3',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q3',key,surveyPoints)
        keyDict['1'] = (surveyQ5,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ5,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ4,('3',False,surveyPoints))
        recordEvent('Timer',key,'surveyQ4','',q4)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question4', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ5('0',False,surveyPoints)

    def surveyQ5(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q5 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q4',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q4',key,surveyPoints)
        keyDict['1'] = (surveyQ6,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ6,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ5,('3',False,surveyPoints))
        recordEvent('Timer',key,'surveyQ5','',q5)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question5', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ6('0',False,surveyPoints)

    def surveyQ6(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q6 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q5',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q5',key,surveyPoints)
        keyDict['1'] = (surveyQ7,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ7,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ7,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ7,('4',True,surveyPoints))
        keyDict['5'] = (surveyQ6,('5',False,surveyPoints))
        recordEvent('Timer',key,'surveyQ6','',q6)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question6', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ7('0',False,surveyPoints)

    def surveyQ7(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q7 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q6',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q6',key,surveyPoints)
        keyDict['1'] = (surveyQ8,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ8,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ8,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ8,('4',True,surveyPoints))
        keyDict['5'] = (surveyQ7,('5',False,surveyPoints))
        keyDict['6'] = (surveyQ8,('6',True,surveyPoints))
        recordEvent('Timer',key,'surveyQ7_edit_2','',q7)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question7_edit', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
        #surveyQ8('0',False,surveyPoints)

    def surveyQ8(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q7_edit_2',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q7_edit_2',key,surveyPoints)
        keyDict = newKeyDict()
        q8 = stopwatch.Timer()
        recordEvent('Timer',key,'surveyQ8','',q8)
        keyDict['1'] = (surveyQ9,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ9,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ9,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ9,('4',True,surveyPoints))
        recordEvent('Timer',key,'gold_q','',q8)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/gold_standard_question', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ9(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q9 = stopwatch.Timer()
        reverseAnswerMapping = {'1': '4', '2': '3', '3':'2', '4': '1'}
        if repeat and (key != '0') and (reverseAnswerMapping[db.getAnswer1(user)] == key):
            if (surveyPoints>5):
                #debugPrint(reverseAnswerMapping[db.getAnswer1(user)])
                db.addSurveyResponse(user,'gold',key,surveyPoints)
                recordEvent('Timer',key,'passed_gold','',q9)
        else:
            #debugPrint(reverseAnswerMapping[db.getAnswer1(user)])
            db.addSurveydUser(user,surveyPoints)
            recordEvent('Timer',key,'failed_gold','',q9)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/mistake_on_gold')
            db.addSurveyResponse(user,'gold',key,surveyPoints)
            hangup()
        keyDict['1'] = (surveyQ10,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ10,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ10,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ10,('4',True,surveyPoints))
        recordEvent('Timer',key,'surveyq9_news','',q9)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question_9_news', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ10(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q9_news',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q9_news',key,surveyPoints)
        keyDict = newKeyDict()
        q10 = stopwatch.Timer()
        recordEvent('Timer',key,'surveyQ10_tv','',q10)
        keyDict['1'] = (surveyQ11,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ11,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ11,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ11,('4',True,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question_10_tv', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)


    def surveyQ11(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q10_tv',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q10_tv',key,surveyPoints)
        keyDict = newKeyDict()
        q11 = stopwatch.Timer()
        recordEvent('Timer',key,'surveyQ11_radio','',q11)
        keyDict['1'] = (surveyQ12,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ12,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ12,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ12,('4',True,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question_11_radio', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)


    def surveyQ12(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q12 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'q11_radio',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'q11_radio',key,surveyPoints)
        keyDict['1'] = (surveyQ13,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ13,('2',True,surveyPoints))
        recordEvent('Timer',key,'pre_test_1','',q12)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/pre_test_1_awareness', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ13(key,repeat,surveyPoints):
        keyDict = newKeyDict()
        q13 = stopwatch.Timer()
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'pre_test_1',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'pre_test_1',key,surveyPoints)
        keyDict['1'] = (surveyQ14,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ14,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ13,('3',False,surveyPoints))
        recordEvent('Timer',key,'pre_test_2','',q13)
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/pre_test_2_quiz', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ14(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'pre_test_2',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'pre_test_2',key,surveyPoints)
        keyDict = newKeyDict()
        q14 = stopwatch.Timer()
        recordEvent('Timer',key,'how_heard','',q14)
        keyDict['1'] = (surveyQ15,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ15,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ15,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ15,('4',True,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question_how_heard', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ15(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'how_heard',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'how_heard',key,surveyPoints)
        keyDict = newKeyDict()
        q15 = stopwatch.Timer()
        recordEvent('Timer',key,'how_spread','',q15)
        recordEvent('Timer',key,'survey_completed','',q15)
        keyDict['1'] = (surveyQ16,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ16,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ16,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ16,('4',True,surveyPoints))
        keyDict['5'] = (surveyQ16,('4',True,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question_how_spread', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ16(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'how_spread',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'how_spread',key,surveyPoints)
        keyDict = newKeyDict()
        q16 = stopwatch.Timer()
        recordEvent('Timer',key,'live_forests','',q16)
        keyDict['1'] = (surveyQ17,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ17,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ16,('3',False,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/live_forests', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ17(key,repeat,surveyPoints):
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'live_forests',key,surveyPoints)
        else:
            db.addSurveyResponse(user,'live_forests',key,surveyPoints)
        keyDict = newKeyDict()
        q17 = stopwatch.Timer()
        recordEvent('Timer',key,'employment','',q17)
        keyDict['1'] = (surveyQ18,('1',True,surveyPoints))
        keyDict['2'] = (surveyQ18,('2',True,surveyPoints))
        keyDict['3'] = (surveyQ18,('3',True,surveyPoints))
        keyDict['4'] = (surveyQ18,('4',True,surveyPoints))
        keyDict['5'] = (surveyQ17,('5',False,surveyPoints))
        for i in range(1,4):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/employment', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ18(key,repeat,surveyPoints):
            if repeat and (key != '0'):
                surveyPoints+=1
                db.addSurveyResponse(user,'employment',key,surveyPoints)
            else:
                db.addSurveyResponse(user,'employment',key,surveyPoints)
            keyDict = newKeyDict()
            q18 = stopwatch.Timer()
            recordEvent('Timer',key,'direct_benefit','',q18)
            keyDict['1'] = (surveyQ19,('1',True,surveyPoints))
            keyDict['2'] = (surveyQ19,('2',True,surveyPoints))
            keyDict['3'] = (surveyQ18,('3',False,surveyPoints))
            for i in range(1,4):
                playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/direct_benefit', keyDict)
                playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)

    def surveyQ19(key,repeat,surveyPoints):
        q9 = stopwatch.Timer()
        reverseAnswerMapping = {'1': '4', '2': '3', '3':'2', '4': '1'}
        if repeat and (key != '0'):
            surveyPoints+=1
            db.addSurveyResponse(user,'direct_benefit',key,surveyPoints)
            db.addSurveydUser(user,surveyPoints)
        else:
            db.addSurveyResponse(user,'direct_benefit',key,surveyPoints)
        recordEvent('Timer',key,'surveyQ19_open','',q9)
        signal.signal(signal.SIGHUP, signal.SIG_IGN)
        while True:
            commentTempFileName = recordFileNoPlayback(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/question8',500)
            if commentTempFileName:
                break
        #Arjun edited to add caller ID in main page
        os.system("echo %s >> /opt/swara/learn2earn.txt" %(user))
        #auth=db.getAuthDetails(user)
        #os.system("echo %s >> /opt/swara/learn2earn.txt" %(auth))

        # convert temp wav file to temp mp3 file
        output=os.popen("/usr/local/bin/lame -h --abr 200 "+
                        AST_SOUND_DIR+commentTempFileName+".wav " +
                        AST_SOUND_DIR+commentTempFileName+".mp3").read().strip()

        # test size of MP3 file
        try:
            audio = MP3(AST_SOUND_DIR+commentTempFileName+".mp3")
            # outside of the training channel, only keep audio files that are longer than 20 seconds
            #if (swaraChannel=="training" or float(audio.info.length) >= 20):
            #newCommentID = db.addCommentToChannel(user, auth, '12345', swaraChannel)
                #newCommentID = db.addCommentToChannel(user, '12345')
            os.rename(AST_SOUND_DIR+commentTempFileName+".mp3", SOUND_DIR+"learn2earn/"+str(user)+".mp3")
            os.rename(AST_SOUND_DIR+commentTempFileName+".wav", SOUND_DIR+str(user)+".wav")
                #os.system("/usr/local/bin/lame -h --abr 200 "+SOUND_DIR+str(newCommentID)+".wav "+SOUND_DIR+"/web/" \
            os.system("echo '%s' >> /var/log/learn2earn.log" %(output))
            #db.addMessageRecordEvent(newCommentID, callID)
        except IOError:
            os.system("IO Error processing MP3 " + AST_SOUND_DIR+commentTempFileName+".mp3 >> /var/log/learn2earn.log")

        if (surveyPoints>7) and (reverseAnswerMapping[db.getAnswer1(user)] == key):
           recharge(user)
           debugPrint("you passed the survey")
        # process hangup again
        signal.signal(signal.SIGHUP, signal.SIG_DFL)
        # server = smtplib.SMTP('smtp.gmail.com:587')
        # server.ehlo()
        # server.starttls()
        # server.ehlo()
        # server.login(username,password)
        # server.sendmail(fromaddr, toaddrs, msg)
        # server.quit()
        #trm = stopwatch.Timer()
        playFile(PROMPTS_DIR+'thank-you-submitted')
        hangup()

        #replace with thank you message
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/survey_questions/survey_begin_again')
    recordEvent('Timer','0','survey begins','',surveyTimer)
    surveyQ1(1,False)

def recordFileNoPlayback(introFilename, recordLen=50000):
    keyDict = newKeyDict()
    name = os.tmpnam()
    name = name[len('/tmp/'):]
    try:
        playFile(introFilename,keyDict)
        # ignore hangup during recording
        debugPrint("start recording");
        recordFile(name, '#1', recordLen, 5)
        debugPrint("done recording");
        # The following code makes it possible for the user to confirm his submission.
        # playFile(name, keyDict)
        #while True:
        #    keyDict['1']= Nop
        #    keyDict['2']= (removeTempFile,(AST_SOUND_DIR+"/"+name+'.wav',))
        #    key = playFileGetKey(PROMPTS_DIR+'submit-or-rerecord', 5000, 1, keyDict)
        #    if key == '1':
        #        return name
        #    elif key == '2':
        #        return None
        #    else:
        #        playFile(PROMPTS_DIR+'not-understood')
        return name
    except KeyPressException, e:
        debugPrint("exception raised");
        if name and os.path.exists(AST_SOUND_DIR+name+'.wav'):
            os.remove(AST_SOUND_DIR+name+'.wav')
        raise

def playEnterNumber(repeat):
    enterNumber = stopwatch.Timer()
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
    if repeat:
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/message_referral_select')
    playFile(PROMPTS_DIR+'learn2earn/HindiRaw/enter_friend_number')
    recordEvent('Timer','0','playedEnterFriendNumber','',enterNumber)
    while (tendigit > 0):
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/empty_pause', keyDict)
          
    if (tendigit == 0):
       keyDict = newKeyDict()
       keyDict['1'] = (playEnterNumber,(False))
       keyDict['2'] = (hangup,())
       global tendigit
       global number
       tendigit = 10
       if db.isCompletedUser(number[1:]):
          number='0'
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/enter_another_friend', keyDict)
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
       else:
          number='0'
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/finished_entering', keyDict)
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
          playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
       recordEvent('Timer','0','finished_entering_number','',enterNumber)
       hangup()

def recordNumber(key):
         recordKey = stopwatch.Timer()
         playFile(PROMPTS_DIR+'learn2earn/HindiRaw/keypress')
         recordEvent('Timer',key,'enterKeyNumber','',recordKey)
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
                db.addReferral(user,number[1:])
                if db.isCompletedUser(user):
                   s = sendSMS(number[1:], 'Van adhikaar anusthaan se sambandhit aasan sawaalon ke sahi jawaab dekar, aapke dost <'+ str(user) +'> abhi abhi 10 rupaiye ka mobile topup jeete hai. Aap bhi sambhashan sunkar, aur sunke kuch sawaalon ke sahi sahi jawaab dekar, 10 rupaiye ke top up jeet sakte hai! sambhashan sunane ke lie <07714233002> par missed call de.')
                else:
                   s = sendSMS(number[1:], 'Aapke dost <'+ str(user) +'> ne aapko 10 rupaiye ka mobile top up jeetne ka avasar diya hai! Aapko keval van adhikar se sambandhit ek sambhashan sunke, kuch aasaan sawaalon ke sahi jawaab dene hai. Toh 10 rupaiye ka top up jeetne ke lie, kripya <07714233002> par missed call kare.')
                db.addReferralSMSStatus(number[1:],s.status_code, s.text)
                signal.signal(signal.SIGHUP, signal.SIG_DFL)


def mainMenu():
    """
    """
    global language
    #callid = db.getID()
    # callid = int(callid) + 1
    tmm = stopwatch.Timer()
    debugPrint("STARTING MAIN MENU")
    language = 'Gondi'
    debugPrint("LANGUAGE IS "+language)
    keyDict = newKeyDict()
    keyDict['1'] = (audioTutorial,())
    keyDict['2'] = (invalidDigit,(2, 'Main Menu', tmm,))
    keyDict['3'] = (invalidDigit,(3, 'Main Menu', tmm,))
    keyDict['4'] = (invalidDigit,(4, 'Main Menu', tmm,))
    keyDict['5'] = (invalidDigit,(5, 'Main Menu', tmm,))
    keyDict['6'] = (invalidDigit,(6, 'Main Menu', tmm,))
    keyDict['7'] = (invalidDigit,(7, 'Main Menu', tmm,))
    keyDict['8'] = (invalidDigit,(8, 'Main Menu', tmm,))
    keyDict['9'] = (invalidDigit,(9, 'Main Menu', tmm,))
    #log_file.write("I am here in the main menu")
    #log_file.flush()
    recordEvent('Timer',1,'Begin intro','',tmm)
    try:
        for i in range(1,3):
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/intro_new', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
        hangup()
    except KeyPressException, e:
        raise


def audioTutorial():
    keyDict = newKeyDict()
    #cdr_id = db.getcallIDByUser(user)
    tutorial = stopwatch.Timer()
    recordEvent('Timer',1,'BeginTutorial','',tutorial)
    ##Abitlity to skip to be removed during deployment
    debugPrint("I am here in audio tutorial beginning")
    #keyDict['1'] = (invalidDigit,(2, 'Main Menu', tm,))
    #keyDict['2'] = (invalidDigit,(2, 'Main Menu', tm,))
    #keyDict['3'] = (invalidDigit,(3, 'Main Menu', tm,))
    #keyDict['4'] = (invalidDigit,(4, 'Main Menu', tm,))
    #keyDict['5'] = (invalidDigit,(5, 'Main Menu', tm,))
    #keyDict['6'] = (invalidDigit,(6, 'Main Menu', tm,))
    keyDict['7'] = (question1,(1,True,))
    #keyDict['8'] = (invalidDigit,(8, 'Main Menu', tm,))
    #keyDict['9'] = (invalidDigit,(9, 'Main Menu', tm,))
    debugPrint("I am here in audio tutorial keydef")
    #log_file.write("I am here audio tutorial")
    #recharge()
    try:
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/conversation_intro')
        recordEvent('Timer',1,'conversation_prompt','',tutorial)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/scenario_final')
        recordEvent('Timer',1,'scenario_ended','',tutorial)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/question_intro')
        recordEvent('Timer',1,'question_intro','',tutorial)
        question1(1,True)
    except KeyPressException, e:
        raise


def question1(key,repeat):

    #debugPrint("I am here in question1:"+key)
    #debugPrint("I am here in after Playing:"+repeat)
    points=0
    keyDict = newKeyDict()
    tm = stopwatch.Timer()
    #cdr_id = db.getcallIDByUser(user)
    debugPrint("I am here after DB")
    recordEvent('Timer',key,'BeginQuestion1','',tm)
    if db.isRetention(user):
       recordEvent('Answer',key,'retention_BeginQuestion1','',tm)
    answers=['Question1_answerchoice_1','Question1_answerchoice_2']
    random.shuffle(answers,random.random)
    debugPrint("I am here after timer")
    keyDict['1'] = (question2,(1,answers[0],True,points,))
    keyDict['2'] = (question2,(2,answers[1],True,points,))
    if repeat is None:
        debugPrint("error repeat is none")
    elif repeat:
        keyDict['3'] = (question1,(3,False))
    else:
        keyDict['3'] = (invalidDigit,(3, 'Question1', tm,))
    keyDict['4'] = (invalidDigit,(4, 'Question1', tm,))
    keyDict['5'] = (invalidDigit,(5, 'Question1', tm,))
    keyDict['6'] = (invalidDigit,(6, 'Question1', tm,))
    keyDict['7'] = (invalidDigit,(7, 'Question1', tm,))
    keyDict['8'] = (invalidDigit,(8, 'Question1', tm,))
    keyDict['9'] = (invalidDigit,(9, 'Question1', tm,))
    debugPrint("I am here before afer keydef:")

    try:
        debugPrint("I am here before Playing:")
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question_1_mixing', keyDict)
        recordEvent('Timer',key,'question1_ended','',tm)
        if db.isRetention(user):
           recordEvent('Timer',key,'retention_question1_ended','',tm)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[0], keyDict)
        recordEvent('Timer',key,'question1_answerchoice1_presented','',tm)
        if db.isRetention(user):
           recordEvent('Timer',key,'retention_question1_answerchoice1_presented','',tm)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_1', keyDict)
        recordEvent('Timer',key,'press1_indicated','',tm)
        if db.isRetention(user):
           recordEvent('Timer',key,'retention_press1_indicated','',tm)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[1], keyDict)
        recordEvent('Timer',key,'question1_answerchoice2_presented','',tm)
        if db.isRetention(user):
           recordEvent('Timer',key,'retention_question1_answerchoice2_presented','',tm)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_2', keyDict)
        if db.isRetention(user):
           recordEvent('Timer',key,'retention_press2_indicated','',tm)
        recordEvent('Timer',key,'press2_indicated','',tm)


        if repeat is None:
            debugPrint("error repeat is none")
        elif repeat:
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/repeat_question', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
            recordEvent('Timer',key,'repeated_question1','',tm)
            if db.isRetention(user):
               recordEvent('Timer',key,'retention_repeated_question1','',tm)
            question1(3,False)
        else:
            question2('','',True,points)
    except KeyPressException, e:
        raise

def question2(key,answer,repeat,points):
    debugPrint("I am here in question2:")
    tq2 = stopwatch.Timer()
    recordEvent('Timer',key,'BeginQuestion2','',tq2)
    if db.isRetention(user):
        recordEvent('Timer',key,'retention_BeginQuestion2','',tq2)
    if repeat is True:
        if answer == 'Question1_answerchoice_1':
            debugPrint("correct answer")
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question1_correct')
            recordEvent('Answer',key,'Question1_correct', answer, tq2)
            if db.isRetention(user):
                recordEvent('Answer',key,'retention_Question1_correct','',tq2)
            points+=1
        else:
            debugPrint("incorrect answer")
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question1_wrong_answer')
            recordEvent('Answer',key,'Question1_incorrect', answer, tq2)
            if db.isRetention(user):
                recordEvent('Answer',key,'retention_Question1_incorrect','',tq2)
    keyDict = newKeyDict()
    #cdr_id = db.getcallIDByUser(user)
    debugPrint("I am here after DB q2")
    answers=['Question2_answerchoice_1','Question2_answerchoice_2']
    random.shuffle(answers,random.random)
    debugPrint("I am here after timer q2")

    keyDict['1'] = (question3,(1,answers[0],True,points))
    keyDict['2'] = (question3,(2,answers[1],True,points))

    if repeat is None:
        debugPrint("error repeat is none")
    elif repeat:
        keyDict['3'] = (question2,(3,'',False,points))
    else:
        keyDict['3'] = (invalidDigit,(3, 'Question2', tq2,))
    keyDict['4'] = (invalidDigit,(4, 'Question2', tq2,))
    keyDict['5'] = (invalidDigit,(5, 'Question2', tq2,))
    keyDict['6'] = (invalidDigit,(6, 'Question2', tq2,))
    keyDict['7'] = (invalidDigit,(7, 'Question2', tq2,))
    keyDict['8'] = (invalidDigit,(8, 'Question2', tq2,))
    keyDict['9'] = (invalidDigit,(9, 'Question2', tq2,))
    debugPrint("I am here before afer keydef: q2")

    try:
        debugPrint("I am here before Playing: q2")
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question_2_mixing', keyDict)
        recordEvent('Timer',key,'question2_ended','',tq2)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question2_ended','',tq2)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[0], keyDict)
        recordEvent('Timer',key,'question2_answerchoice1_presented','',tq2)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question2_answerchoice1_presented','',tq2)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_1', keyDict)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_press1_indicated','',tq2)
        recordEvent('Timer',key,'press1_indicated','',tq2)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[1], keyDict)
        recordEvent('Timer',key,'question2_answerchoice2_presented','',tq2)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question2_answerchoice2_presented','',tq2)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_2', keyDict)
        recordEvent('Timer',key,'press2_indicated','',tq2)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_press2_indicated','',tq2)

        if repeat is None:
            debugPrint("error repeat is none")
        elif repeat:
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/repeat_question', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
            recordEvent('Timer',key,'repeated_question2','',tq2)
            if db.isRetention(user):
                recordEvent('Timer',key,'retention_repeated_question2','',tq2)
            question2(3,'',False,points)
        else:
            question3('','',True,points)
    except KeyPressException, e:
        raise

def question3(key,answer,repeat,points):
    debugPrint("I am here in question3:")
    tq3 = stopwatch.Timer()
    recordEvent('Timer',key,'BeginQuestion3','',tq3)
    if db.isRetention(user):
                recordEvent('Timer',key,'retention_BeginQuestion3','',tq3)
    if repeat is True:
        if answer == 'Question2_answerchoice_1':
            debugPrint("correct answer")
            recordEvent('Answer',key,'question2_correct', answer, tq3)
            if db.isRetention(user):
                recordEvent('Answer',key,'retention_question2_correct','',tq3)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question2_right_answer')
            points+=1
        else:
            debugPrint("incorrect answer")
            recordEvent('Answe',key,'question2_incorrect', answer, tq3)
            if db.isRetention(user):
                recordEvent('Answer',key,'retention_question2_incorrect','',tq3)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question2_wrong_answer')
    keyDict = newKeyDict()
    #cdr_id = db.getcallIDByUser(user)
    debugPrint("I am here after DB q3")
    answers=['Question3_answerchoice_1','Question3_answerchoice_2']
    random.shuffle(answers,random.random)
    debugPrint("I am here after timer q3")

    keyDict['1'] = (checkTopup,(1,answers[0],True,points))
    keyDict['2'] = (checkTopup,(2,answers[1],True,points))

    if repeat is None:
        debugPrint("error repeat is none")
    elif repeat:
        keyDict['3'] = (question3,(3,'',False,points))
    else:
        keyDict['3'] = (invalidDigit,(3, 'Question3', tq3,))
    keyDict['4'] = (invalidDigit,(4, 'Question3', tq3,))
    keyDict['5'] = (invalidDigit,(5, 'Question3', tq3,))
    keyDict['6'] = (invalidDigit,(6, 'Question3', tq3,))
    keyDict['7'] = (invalidDigit,(7, 'Question3', tq3,))
    keyDict['8'] = (invalidDigit,(8, 'Question3', tq3,))
    keyDict['9'] = (invalidDigit,(9, 'Question3', tq3,))
    debugPrint("I am here before afer keydef: q3")

    try:
        debugPrint("I am here before Playing: q3")
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question_3_mixing', keyDict)
        recordEvent('Timer',key,'question3_ended','',tq3)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question3_ended','',tq3)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[0], keyDict)
        recordEvent('Timer',key,'question3_answerchoice1_presented','',tq3)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question3_answerchoice1_presented','',tq3)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_1', keyDict)
        recordEvent('Timer',key,'press1_indicated','',tq3)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_press1_indicated','',tq3)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/'+answers[1], keyDict)
        recordEvent('Timer',key,'question3_answerchoice2_presented','',tq3)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_question3_answerchoice2_presented','',tq3)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/press_2', keyDict)
        recordEvent('Timer',key,'press2_indicated','',tq3)
        if db.isRetention(user):
                recordEvent('Timer',key,'retention_press2_indicated','',tq3)

        if repeat is None:
            debugPrint("error repeat is none")
        elif repeat:
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/repeat_question', keyDict)
            playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
            recordEvent('Answer',key,'repeated_question3','',tq3)
            if db.isRetention(user):
                recordEvent('Answer',key,'retention_repeated_question3','',tq3)
            question3(3,'',False,points)
        else:
            checkTopup('','',True,points)
    except KeyPressException, e:
        raise


def checkTopup(key,answer,repeat,points):
    debugPrint("I am here topup")
    ### Question 5 answer missing, please record####
    #playFile(PROMPTS_DIR+'learn2earn/Question5_answer')
    end = stopwatch.Timer()
    recordEvent('Timer',key,'checkTopUpBegins','',end)
    if db.isRetention(user):
                recordEvent('Timer',key,'retention_checkTopUpBegins','',end)
    if answer == 'Question3_answerchoice_1':
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question3_right_answer')
        recordEvent('Answer',key,'question3_correct', answer, end)
        if db.isRetention(user):
                recordEvent('Answer',key,'retention_question3_correct','',end)
        points+=1
    else:
        debugPrint("incorrect answer")
        recordEvent('Answer',key,'question3_incorrect', answer, end)
        if db.isRetention(user):
                recordEvent('Answer',key,'retention_question3_incorrect','',end)
        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Question3_wrong_answer')
    #keyDict = newKeyDict()
    #cdr_id = db.getcallIDByUser(user)
    debugPrint("I am here after DB topup")
    #keyDict['1'] = (recordFollowup,())
    if db.isRetention(user):
                recordEvent('Timer',key,'retention_completed','',end)
                db.addRetentionPoints(user,points)

    try:
        if points == 3:
           playFile(PROMPTS_DIR+'learn2earn/HindiRaw/congrats_new')
           #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/earning_opportunities')
           signal.signal(signal.SIGHUP, signal.SIG_IGN)
           recordEvent('Timer',key,'played_congrats','',end)
           if db.isRetention(user):
                recordEvent('Timer',key,'retention_played_congrats','',end)
                s = sendSMS(user, 'Mubarak ho! Aapne van adhikar ka adhyay dobara safaltapoorvak poorna kiya hai.')
                recharge(user)
           # ignore hangup during recording
           else:
                s = sendSMS(user, 'Mubarak ho! Aapne van adhikar ka adhyay safaltapoorvak poorna kiya hai. Apne dost parivar ko fatafat 07714233002 par missed call dene ke lie kahiye,  taki vo bhi ye sambhashan sunkar van adhikar ke bare me jagruk ho.')
                db.addSMSStatus(user,s.status_code, s.text)
                recordEvent('Timer',key,'sms_sent','',end)
           #check if they got the money already!
           # if not db.isRechargedUser(user):
           #        recharge(user)
           # else:
           #        playFile(PROMPTS_DIR+'learn2earn/HindiRaw/recharge_already_done')
           # recordEvent('Timer',key,'recharge_checked','',end)
           # if db.isReferredUser(user):
           #    friend = db.getReferrer(user)
           #    recordEvent('Timer','0','identified friend referrer',friend,end)
           #    recharge(friend)
           #    recordEvent('Timer','0','recharged friend referrer',friend,end)
           #    t = sendSMS(db.getReferrer(user), 'Mubarak ho! Aapke dost <'+user+'> ne sare sawaalon ke sahi jawaab diye hai. Thodi hi der me, aapko 10 rupaiye ka mobile top up milega. Humari madat karne ke lie shukriya!')
           #    db.addAckRefSMS(db.getReferrer(user),user,t.status_code, t.text)
           #recordEvent('Timer',key,'smss_sent','',end)
           recordEvent('Timer',key,'learn2earn_completed','',end)
           if db.isRetention(user):
                recordEvent('Timer',key,'retention_learn2earn_completed','',end)
           # process hangup again
           signal.signal(signal.SIGHUP, signal.SIG_DFL)
           if db.isRetention(user):
                playFile(PROMPTS_DIR+'learn2earn/HindiRaw/end_message_retention')
           else:
                playFile(PROMPTS_DIR+'learn2earn/HindiRaw/end_message_new')
           hangup()
        if points < 3:
           playFile(PROMPTS_DIR+'learn2earn/HindiRaw/Quiz_fail')
           recordEvent('Timer',key,'quiz_failed','',end)
           if points == 2:
               playFile(PROMPTS_DIR+'learn2earn/HindiRaw/two')
           elif points < 2:
               playFile(PROMPTS_DIR+'learn2earn/HindiRaw/one')
           elif points < 1:
               playFile(PROMPTS_DIR+'learn2earn/gondi_raw/zero')
           playFile(PROMPTS_DIR+'learn2earn/HindiRaw/come_again_later_new')
           recordEvent('Timer',key,'played_come_again_later','',end)
           if db.isRetention(user):
                recordEvent('Timer',key,'retention_played_come_again_later','',end)
                #recharge(user)
           #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/referral_program')
           #playFile(PROMPTS_DIR+'learn2earn/HindiRaw/5sec_wait', keyDict)
           recordEvent('Timer',key,'learn2earn_completed','',end)
           hangup()
    except KeyPressException, e:
        raise

def recharge(user):
    number = user
    n = requests.get('http://api.datayuge.in/v6//mnp?apikey=hWIjrc064jHVkIzZv7SJQz1bmlQuZPWb&number='+number)
    operator_data = json.loads(n.text)
    if (operator_data['circle'] == 'Madhya Pradesh Chhattisgarh') or (operator_data['circle'] == 'Bihar Jharkhand') or (operator_data['circle'] == 'Orissa'):
        r = requests.get ('http://smsalertbox.com/api/recharge.php?uid=67616e65736169&pin=4634e1e3b8e8d520aa239055d202fe8b&number='+number+'&operator='+str(Operators[operator_data['operator']])+'&circle='+str(Circles[operator_data['circle']])+'&amount=10&usertx='+str(random_with_N_digits(20))+'&format=json&version=4')
        recharge_status = json.loads(r.text)
        db.addRechargeStatus(recharge_status['txid'], recharge_status['user_txid'], recharge_status['status'], recharge_status['amount'], recharge_status['your_cost'], recharge_status['balance'], recharge_status['number'], recharge_status['operator'], recharge_status['operator_ref'], recharge_status['error_code'], recharge_status['message'], operator_data['circle'], operator_data['operator'],user)
        debugPrint(r.text)
    #db.addRechargeStatus


def sendSMS(number, message):
    data = {'user': "arvindkhadri", 'passwd': "59849764", 'message': message, 'mobilenumber':number, 'mtype':'N', 'DR':'Y'}
    sms = requests.get("http://api.smscountry.com/SMSCwebservice_bulk.aspx", params=data, timeout=60)
    if sms.status_code == 200:
        return sms
    else:
        return False


def recordFollowup():
    db.addFollowUser(user)
    hangup()

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)


def invalidDigit(key, context, time):
    # keyDict3 = newKeyDict()
    # playFile(PROMPTS_DIR+'this-cgnet-swara', keyDict3)
    #db.addInvalidkeyEvent(key, context, time) Arjun Patched with CallID
    db.addInvalidkeyEvent(key, context, time, callID)
    # if (str(context)=='mainMenu'):
        # try:
            # playFile(PROMPTS_DIR+'welcome',keyDict)
            # for i in range(1,4):
                # playFile(PROMPTS_DIR+'record-1', keyDict)
            # hangup()
    # elif (str(context)=='playBack'):
        # playBack()
    # elif (str(context)=='addComment'):
        # addComment()
    # else:
        # login()

def recordEvent(eventype, key, context, answer, time):
    #t = stopwatch.Timer()
    # keyDict = newKeyDict()
    # keyDict['8'] = (recordEvent,(8,callID))
    debugPrint("From learn2earn User event %c " % (chr(int(key))))
    db.addEvent(eventype,key, context, answer, time, callID, user)


### procedural code starts here ###

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
    login()
    while True:
        try:
            mainMenu()
        except KeyPressException, e:
            if e.key != '0':
                #db.addInvalidkeyEvent(e.key, 'mm', 5) Arjun patched with CallID
                db.addInvalidkeyEvent(e.key, 'mm', 5, callID)
            else:
                continue
    hangup()

