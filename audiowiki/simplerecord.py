#!/usr/bin/python
# -*- coding: utf-8 -*-

# a simple script requested by Devansh for recording an audio file and
# putting it in a directory

import smtplib
import sys
import stopwatch
import os
import signal
import re
import time
import random
import copy
import sendSMS
from utilities import *
from asteriskinterface import *
from mutagen.mp3 import MP3

language = 'kannada' # Default language is kannada
SOUND_DIR = '/var/lib/asterisk/sounds/audiowikiIndia/'
PROMPTS_DIR = SOUND_DIR + 'prompts/main/' # extended during setup
AST_SOUND_DIR = '/var/lib/asterisk/sounds/'

sys.setrecursionlimit(15000)

f12 = open("tryit123.txt","w")
f12.write("tryit123")

##### State functions ######

def playBack(intro=None):
    keyDict = newKeyDict()
    cdr_id = db.getcallIDByUser(user)
    countKeyPress(2, cdr_id)
    # temporary fix so that incoming calls have a user
    posts = db.getPostsInChannel('12345', swaraChannel, user)
    if len(posts) == 0:
        return playFile(PROMPTS_DIR+'no-comments', keyDict)
    playFile(PROMPTS_DIR+'mistake-0', keyDict)
    playFile(PROMPTS_DIR+intro, keyDict)
    count = 0
    for postID in posts:
        tpb = stopwatch.Timer()
        count = count + 1
        if (count==13):
            break
        keyDict['1'] = (skipComment,(postID, tpb))
        keyDict['3'] = (invalidDigit,(3, 'Playback', tpb,))
        keyDict['4'] = (invalidDigit,(4, 'Playback', tpb,))
        keyDict['5'] = (invalidDigit,(5, 'Playback', tpb,))
        keyDict['6'] = (invalidDigit,(6, 'Playback', tpb,))
        keyDict['7'] = (invalidDigit,(7, 'Playback', tpb,))
        keyDict['8'] = (countKeyPress,(8,cdr_id))
        keyDict['9'] = (invalidDigit,(9, 'Playback', tpb,))
        commentFile = SOUND_DIR+str(postID)
        keyPress = '8'
        while keyPress == '8':
            keyPress = playFile(commentFile, keyDict)
        
        if keyPress == '1': # If user presses 1, skip to next comment.
            pass
        
        db.addPlaybackEvent(postID, tpb, callID) #ARJUN PATCHED with CallID
    tpbm = stopwatch.Timer()
    playFile(PROMPTS_DIR+'for-older-posts')
    keyDict2 = newKeyDict()
    keyDict2['1'] = (addComment,())
    keyDict2['2'] = (playBack,('skip-post-1',))
    keyDict2['3'] = (playBackImpact,('skip-post-1',))
    keyDict2['4'] = (invalidDigit,(4, 'Main Menu after Playback', tpbm,))
    keyDict2['5'] = (invalidDigit,(5, 'Main Menu after Playback', tpbm,))
    keyDict2['6'] = (invalidDigit,(6, 'Main Menu after Playback', tpbm,))
    keyDict2['7'] = (invalidDigit,(7, 'Main Menu after Playback', tpbm,))
    keyDict2['8'] = (invalidDigit,(8, 'Main Menu after Playback', tpbm,))
    keyDict2['9'] = (invalidDigit,(9, 'Main Menu after Playback', tpbm,))
    playFile(PROMPTS_DIR+'this-cgnet-swara', keyDict2)
    for i in range(1,4):
        playFile(PROMPTS_DIR+'record-1', keyDict2)
        playFile(PROMPTS_DIR+'listen-2', keyDict2)
        playFile(PROMPTS_DIR+'impact-3', keyDict)
        playFile(PROMPTS_DIR+'wait-5-seconds', keyDict2)
    hangup()

def playBackImpact(intro=None):
    keyDict = newKeyDict()
    cdr_id = db.getcallIDByUser(user)
    countKeyPress(3, cdr_id)
    # temporary fix so that incoming calls have a user
    posts = db.getImpactPostsInChannel('12345', swaraChannel, user)
    if len(posts) == 0:
        return playFile(PROMPTS_DIR+'no-comments', keyDict)
    playFile(PROMPTS_DIR+'mistake-0', keyDict)
    playFile(PROMPTS_DIR+intro, keyDict)
    count = 0
    for postID in posts:
        tpb = stopwatch.Timer()
        count = count + 1
        if (count==12):
            break
        keyDict['1'] = (skipComment,(postID, tpb))
        keyDict['3'] = (invalidDigit,(3, 'Playback', tpb,))
        keyDict['4'] = (invalidDigit,(4, 'Playback', tpb,))
        keyDict['5'] = (invalidDigit,(5, 'Playback', tpb,))
        keyDict['6'] = (invalidDigit,(6, 'Playback', tpb,))
        keyDict['7'] = (invalidDigit,(7, 'Playback', tpb,))
        keyDict['8'] = (countKeyPress,(8,cdr_id))
        keyDict['9'] = (invalidDigit,(9, 'Playback', tpb,))
        commentFile = SOUND_DIR+str(postID)
        keyPress = '8'
        while keyPress == '8':
            keyPress = playFile(commentFile, keyDict)
        
        if keyPress == '1': # If user presses 1, skip to next comment.
            pass
        
        db.addImpactPlaybackEvent(postID, tpb, callID) #ARJUN PATCHED with CallID
    tpbm = stopwatch.Timer()
    playFile(PROMPTS_DIR+'for-older-posts')
    keyDict2 = newKeyDict()
    keyDict2['1'] = (addComment,())
    keyDict2['2'] = (playBack,('skip-post-1',))
    keyDict2['3'] = (playBackImpact,('skip-post-1',))
    keyDict2['4'] = (invalidDigit,(4, 'Main Menu after Playback', tpbm,))
    keyDict2['5'] = (invalidDigit,(5, 'Main Menu after Playback', tpbm,))
    keyDict2['6'] = (invalidDigit,(6, 'Main Menu after Playback', tpbm,))
    keyDict2['7'] = (invalidDigit,(7, 'Main Menu after Playback', tpbm,))
    keyDict2['8'] = (invalidDigit,(8, 'Main Menu after Playback', tpbm,))
    keyDict2['9'] = (invalidDigit,(9, 'Main Menu after Playback', tpbm,))
    playFile(PROMPTS_DIR+'this-cgnet-swara', keyDict2)
    for i in range(1,4):
        playFile(PROMPTS_DIR+'record-1', keyDict2)
        playFile(PROMPTS_DIR+'listen-2', keyDict2)
        playFile(PROMPTS_DIR+'impact-3', keyDict)
        playFile(PROMPTS_DIR+'wait-5-seconds', keyDict2)
    hangup()


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

def skipComment(commentID, time):
    debugPrint("SKIPPING COMMENT "+str(commentID))
    db.skipComment(int(commentID))

    #db.addSkipEvent(commentID, time, callID) Arjun patchd with CallID
    db.addSkipEvent(commentID, time, callID)

def addComment():
    # ignore hangup during recording
    signal.signal(signal.SIGHUP, signal.SIG_IGN)
    while True:
        commentTempFileName = recordFileNoPlayback(PROMPTS_DIR+'record-message-beep',300)
        if commentTempFileName:
            break

    # convert temp wav file to temp mp3 file
    output=os.popen("/usr/local/bin/lame -h --abr 200 "+
                    AST_SOUND_DIR+commentTempFileName+".wav " +
                    AST_SOUND_DIR+commentTempFileName+".mp3").read().strip()

    # test size of MP3 file
    try:
        #newCommentID = db.addCommentToChannel(user, '12345')
        os.rename(AST_SOUND_DIR+commentTempFileName+".mp3", SOUND_DIR+"recordings/"+commentTempFileName+".mp3")
    except IOError:
        os.system("IO Error processing MP3 " + AST_SOUND_DIR+commentTempFileName+".mp3 >> /var/log/swara.log")

    # process hangup again
    signal.signal(signal.SIGHUP, signal.SIG_DFL)
    # server = smtplib.SMTP('smtp.gmail.com:587')
    # server.ehlo()
    # server.starttls()
    # server.ehlo()
    # server.login(username,password)
    # server.sendmail(fromaddr, toaddrs, msg)
    # server.quit()
    playFile(PROMPTS_DIR+'thank-you-submitted')
    hangup()
    quit()
    exit()

def recordFileNoPlayback(introFilename, recordLen=30000):
    keyDict = newKeyDict()
    name = os.tmpnam()
    name = name[len('/tmp/'):]
    try:
        playFile(introFilename,keyDict)
        # ignore hangup during recording
        recordFile(name, '#1', recordLen, 5)
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

def countKeyPress(key,callID):
    t = stopwatch.Timer()
    # keyDict = newKeyDict()
    # keyDict['8'] = (countKeyPress,(8,callID))
    debugPrint("From main_menu.py User pressed %c " % (chr(int(key))))
    db.recordKeyPress(key, user, callID)


def checkCaller(signum, frame):
    """Check if the call exists in keyPress table, if yes then send
    them an SMS about the number of times they pressed the key 8"""
    # if(db.isCurrentCall(callID)):
    #     #sendSMS()
    #     debugPrint("Send sms for this callID {0}".format(callID))
    if db.getCountKeyPress(user) is not None and db.getCountKeyPress(user) >= 0: 
        count = db.getCountKeyPress(user)
        count = count + 1 #Increase the counter as it was started from 0.
        key = 8
        message = 'Hi, you pressed key {0}, {1} times.'.format(key, count)
        if len(user) == 12:
            sendSMS.sendSMS(user.lstrip('91'), message)
        else:
            sendSMS.sendSMS(user, message)
        db.removeUserfromKeypress(user)
    exit() #exit as the user has disconnected the call.


### procedural code starts here ###

if __name__=='__main__':
    # Read and ignore AGI environment (read until blank line)
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
    user = env['agi_callerid']
    # if user isn't detected by callerid, get it from the argument list
    if (user == "unknown" or user == "100"):
        user = env['agi_arg_2']
    addComment()
    hangup()

