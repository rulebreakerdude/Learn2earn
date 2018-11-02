#DB Functions

#import * safe
import MySQLdb
import re
from datetime import date, timedelta
from utilities import *

#DB_USER = 'flash'
#DB_PASSWD = 'Ath3n@1094'
DB_USER = 'root'
DB_PASSWD = 'apVa25aC#'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'learn2earn'


class Database:
    def __init__(self, db_name=DB_NAME,db_user=DB_USER):
        db_port=DB_PORT
        db_host=DB_HOST
        db_passwd=DB_PASSWD
        self.db = MySQLdb.connect(port=db_port,host=db_host,
                                user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')


    def newCall(self, user):
        self.c.execute("INSERT INTO callLog (user) values (%s);",(str(user),))
        self.db.commit()
        #Arjun patched for analytics
        self.c.execute("SELECT LAST_INSERT_ID() FROM callLog;")
        callID=self.c.fetchall()
        callID=[i[0] for i in callID]
        return callID[0]

    def addSurveyResponse(self,user,question,answer,points):
        self.c.execute("INSERT INTO surveyResponse (user, question, answer,points) VALUES (%s, %s, %s, %s);" ,(str(user), str(question), str(answer), str(points)))
        self.db.commit()

    def addUser(self, phoneNumberString):
        self.c.execute("INSERT INTO users (phone_number) " + \
                       "VALUES (%s);",(str(phoneNumberString),))
        self.db.commit()

    def addFollowUser(self, phoneNumberString):
        self.c.execute("INSERT INTO followup (phone_number) " + \
                       "VALUES (%s);",(str(phoneNumberString),))
        self.db.commit()




    def isUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM users WHERE phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def addReferral(self, user, phoneNumberString):
        self.c.execute("INSERT INTO invites (user,referral) " + \
                       "VALUES (%s, %s);",(str(user),str(phoneNumberString),))
        self.db.commit()

    def isCompletedUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT DISTINCT phoneNumber FROM eventLog WHERE context='played_congrats'AND phoneNumber= %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isSurveyCompleted(self, phoneNumberString):
        count = self.c.execute(
            "SELECT user FROM surveyCompleted WHERE user = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def addSurveydUser(self, phoneNumberString, points):
        self.c.execute("INSERT INTO surveyCompleted (user,points) " + \
                       "VALUES (%s, %s);",(str(phoneNumberString),str(points),))
        self.db.commit()

    def isReferredUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT referral FROM invites WHERE referral = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def rechargeExists(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phoneNumber FROM rechargeStatus WHERE phoneNumber = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def passedQuiz(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phoneNumber FROM eventLog WHERE context='played_congrats' and phoneNumber = %s;"
                                            ,(str(phoneNumberString),))
        return count>0


    def isSurveyTaken(self, phoneNumberString):
        count = self.c.execute(
            "SELECT user FROM surveyCompleted WHERE user = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isRetention(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM retention WHERE phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isTB(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM tb_100 WHERE phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def addTBStatus(self,user,status,text):
        self.c.execute("INSERT INTO TB_SMS_Status (user,status, text) VALUES (%s, %s, %s);" ,(str(user), str(status), str(text),))
        self.db.commit()

    def addRetStatus(self,user,status,text):
        self.c.execute("INSERT INTO retention_status (user,status, text) VALUES (%s, %s, %s);" ,(str(user), str(status), str(text),))
        self.db.commit()

    def isTBCompleted(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM tb_responses WHERE response='2' and phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isRetentionCompleted(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phone_number FROM retention_responses WHERE response='3' and phone_number = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isLegitimateSurvey(self, phoneNumberString):
        count = self.c.execute(
            "SELECT user FROM surveyResponse WHERE question='pre_test_1' and user = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def isAmongLastThree(self, phoneNumberString):
        count = self.c.execute(
            "SELECT user FROM surveyResponse WHERE question='live_forests' and user = %s;"
                                            ,(str(phoneNumberString),))
        return count>0

    def getState(self, phoneNumberString):
        state = self.c.execute(
            "SELECT circle FROM rechargeStatus WHERE phoneNumber = %s;"
                                            ,(str(phoneNumberString),))
        state = self.c.fetchall()
        state =[i[0] for i in state]
        return state[0]

    def getAge(self, phoneNumberString):
        age = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q1'and user= %s;"
                                            ,(str(phoneNumberString),))
        age = self.c.fetchall()
        age =[i[0] for i in age]
        return age[0]

    def getInviteCount(self, phoneNumberString):
        count = self.c.execute(
            "SELECT count(*) FROM `invites` where user= %s;"
                                            ,(str(phoneNumberString),))
        count = self.c.fetchall()
        count =[i[0] for i in count]
        return count[0]

    def getCamera(self, phoneNumberString):
        camera = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q2'and user= %s;"
                                            ,(str(phoneNumberString),))
        camera = self.c.fetchall()
        camera =[i[0] for i in camera]
        return camera[0]

    def getTouchScreen(self, phoneNumberString):
        touchScreen = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q3'and user= %s;"
                                            ,(str(phoneNumberString),))
        touchScreen = self.c.fetchall()
        touchScreen =[i[0] for i in touchScreen]
        return touchScreen[0]

    def getSMS(self, phoneNumberString):
        sms = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q4'and user= %s;"
                                            ,(str(phoneNumberString),))
        sms = self.c.fetchall()
        sms =[i[0] for i in sms]
        return sms[0]

    def getFB(self, phoneNumberString):
        fb = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q5'and user= %s;"
                                            ,(str(phoneNumberString),))
        fb = self.c.fetchall()
        fb =[i[0] for i in fb]
        return fb[0]

    def getEducation(self, phoneNumberString):
        education = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q6'and user= %s;"
                                            ,(str(phoneNumberString),))
        education = self.c.fetchall()
        education =[i[0] for i in education]
        return education[0]

    def getIncome(self, phoneNumberString):
        income = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q7_edit_2'and user= %s;"
                                            ,(str(phoneNumberString),))
        income = self.c.fetchall()
        income =[i[0] for i in income]
        return income[0]

    def getNews(self, phoneNumberString):
        news = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q9_news'and user= %s;"
                                            ,(str(phoneNumberString),))
        news = self.c.fetchall()
        news =[i[0] for i in news]
        return news[0]

    def getTv(self, phoneNumberString):
        tv = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q10_tv'and user= %s;"
                                            ,(str(phoneNumberString),))
        tv = self.c.fetchall()
        tv =[i[0] for i in tv]
        return tv[0]

    def getRadio(self, phoneNumberString):
        radio = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='q11_radio'and user= %s;"
                                            ,(str(phoneNumberString),))
        radio = self.c.fetchall()
        radio =[i[0] for i in radio]
        return radio[0]

    def getPretest1(self, phoneNumberString):
        pre_test_1 = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='pre_test_1'and user= %s;"
                                            ,(str(phoneNumberString),))
        pre_test_1 = self.c.fetchall()
        pre_test_1 =[i[0] for i in pre_test_1]
        return pre_test_1[0]

    def getPretest2(self, phoneNumberString):
        pre_test_2 = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='pre_test_2'and user= %s;"
                                            ,(str(phoneNumberString),))
        pre_test_2 = self.c.fetchall()
        pre_test_2 =[i[0] for i in pre_test_2]
        return pre_test_2[0]

    def getHowHeard(self, phoneNumberString):
        how_heard = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='how_heard'and user= %s;"
                                            ,(str(phoneNumberString),))
        how_heard = self.c.fetchall()
        how_heard =[i[0] for i in how_heard]
        return how_heard[0]

    def getHowSpread(self, phoneNumberString):
        how_spread = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='how_spread'and user= %s;"
                                            ,(str(phoneNumberString),))
        how_spread = self.c.fetchall()
        how_spread =[i[0] for i in how_spread]
        return how_spread[0]

    def getLiveForests(self, phoneNumberString):
        live_forests = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='live_forests'and user= %s;"
                                            ,(str(phoneNumberString),))
        live_forests = self.c.fetchall()
        live_forests =[i[0] for i in live_forests]
        return live_forests[0]

    def getEmployment(self, phoneNumberString):
        employment = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='employment'and user= %s;"
                                            ,(str(phoneNumberString),))
        employment = self.c.fetchall()
        employment =[i[0] for i in employment]
        return employment[0]

    def getDirectBenefit(self, phoneNumberString):
        direct_benefit = self.c.execute(
            "SELECT answer FROM surveyResponse WHERE question='direct_benefit'and user= %s;"
                                            ,(str(phoneNumberString),))
        direct_benefit = self.c.fetchall()
        direct_benefit =[i[0] for i in direct_benefit]
        return direct_benefit[0]

    def countInvited(self, phoneNumberString):
        countInvited = self.c.execute(
            "SELECT count(*) FROM invites WHERE user= %s;"
                                            ,(str(phoneNumberString),))
        countInvited = self.c.fetchall()
        countInvited =[i[0] for i in countInvited]
        return countInvited[0]

    def countReferrals(self, phoneNumberString):
        suc_ref = self.c.execute(
            "SELECT count(*) FROM ackRefSMS WHERE user= %s;"
                                            ,(str(phoneNumberString),))
        suc_ref = self.c.fetchall()
        suc_ref =[i[0] for i in suc_ref]
        return suc_ref[0]

    def getRechargeStatus(self, phoneNumberString):
        status = self.c.execute(
            "SELECT status FROM rechargeStatus WHERE phoneNumber= %s;"
                                            ,(str(phoneNumberString),))
        status = self.c.fetchall()
        status =[i[0] for i in status]
        return status[0]

    def insertTB100(self):
        self.c.execute("INSERT INTO tb_100 (userid,phone_number,lastloggedin) SELECT id,phone_number,lastloggedin FROM paid_users WHERE phone_number not in (select phone_number from tb_100) and phone_number not in (select phone_number from retention)  order by rand() limit 2")
        #insert = self.c.fetchall()
        #insert =[i[0] for i in insert]
        self.db.commit()

    def insertRetention(self):
        self.c.execute("INSERT INTO retention (userid,phone_number,lastloggedin) SELECT id,phone_number,lastloggedin FROM paid_users WHERE phone_number not in (select phone_number from tb_100) and phone_number not in (select phone_number from retention)  order by rand() limit 2")
        #self.c.execute("ALTER TABLE `retention` AUTO_INCREMENT = 1;INSERT INTO retention (userid,phone_number,lastloggedin) SELECT id,phone_number,lastloggedin FROM paid_users WHERE phone_number not in (select phone_number from tb_100) and phone_number not in (select phone_number from retention)  order by rand() limit 100")
        #insert = self.c.fetchall()
        #insert =[i[0] for i in insert]
        self.db.commit()

    def addTBResponse(self,user, response):
        self.c.execute("INSERT INTO tb_responses (phone_number, response) VALUES (%s, %s);" ,(str(user), str(response)))
        self.db.commit()

    def addRetentionPoints(self,user, points):
        self.c.execute("INSERT INTO retention_responses (phone_number, response) VALUES (%s, %s);" ,(str(user), str(points)))
        self.db.commit()

    def getTb100(self):
        tb100 = self.c.execute(
            "SELECT phone_number FROM tb_100 WHERE id > (SELECT MAX(id) - 2 FROM tb_100)",())
        tb100 = self.c.fetchall()
        tb100 =[i[0] for i in tb100]
        return tb100

    def getRetention100(self):
        ret100 = self.c.execute(
            "SELECT phone_number FROM retention WHERE id > (SELECT MAX(id) - 2 FROM tb_100)",())
        ret100 = self.c.fetchall()
        ret100 =[i[0] for i in ret100]
        return ret100

    def getCallCount(self, phoneNumberString):
        call_count = self.c.execute(
            "SELECT count(*) FROM callLog WHERE user= %s;"
                                            ,(str(phoneNumberString),))
        call_count = self.c.fetchall()
        call_count =[i[0] for i in call_count]
        return call_count[0]

    def getLastCalled(self, phoneNumberString):
        last_call = self.c.execute(
            "SELECT lastloggedin FROM users WHERE phone_number= %s;"
                                            ,(str(phoneNumberString),))
        last_call = self.c.fetchall()
        last_call =[i[0] for i in last_call]
        return last_call[0]

    def getQuizTime(self, phoneNumberString):
        quiz_time = self.c.execute(
            "SELECT timeOfEvent FROM eventLog WHERE context='played_congrats' and phoneNumber= %s group by phoneNumber;"
                                            ,(str(phoneNumberString),))
        quiz_time = self.c.fetchall()
        quiz_time =[i[0] for i in quiz_time]
        return quiz_time[0]

    def getRechargeCount(self, phoneNumberString):
        count = self.c.execute(
            "SELECT count(*) FROM rechargeStatus WHERE phoneNumber = %s;"
                                            ,(str(phoneNumberString),))
        count = self.c.fetchall()
        count =[i[0] for i in count]
        return count[0]

    def getReferrer(self, phoneNumberString):
        referrer = self.c.execute(
            "SELECT user FROM invites WHERE referral = %s;"
                                            ,(str(phoneNumberString),))
        referrer = self.c.fetchall()
        referrer =[i[0] for i in referrer]
        return referrer[0]

    def getAnswer1(self, phoneNumberString):
        answer = self.c.execute(
            "SELECT answer FROM surveyResponse where question='q1' and user = %s;"
                                            ,(str(phoneNumberString),))
        answer = self.c.fetchall()
        answer =[i[0] for i in answer]
        return answer[0]

    def isRechargedUser(self, phoneNumberString):
        count = self.c.execute(
            "SELECT phoneNumber FROM rechargeStatus WHERE phoneNumber = %s AND status = 'SUCCESS';"
                                            ,(str(phoneNumberString),))
        return count>0

    def addInvalidkeyEvent(self, key, when, duration, callid):
        self.c.execute("INSERT INTO analytics (eventype, invdgtpsd, context, whenpressed,callid) VALUES (%s, %s, %s, %s, %s);" ,('Invalid Keypress', str(key), str(when), str(duration),str(callid),))
        self.db.commit()

    def addEvent(self, eventype, key, when, answer, duration, callid, user):
        self.c.execute("INSERT INTO eventLog (eventype, invdgtpsd, context, answer, whenpressed,callid,phoneNumber) VALUES (%s, %s, %s, %s, %s, %s, %s);" ,(str(eventype), str(key), str(when), str(answer), str(duration),str(callid), str(user),))
        self.db.commit()

    def addRechargeStatus(self, txid, usertxid, status, amount, your_cost, balance, number, operator, operatorref, errorcode, message, circle, network, user):
        self.c.execute("INSERT INTO rechargeStatus (txid, user_txid, status, amount, your_cost, balance, number, operator, operator_ref, error_code, message, circle, network, phoneNumber) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);" ,(str(txid), str(usertxid), str(status), str(amount), str(your_cost), str(balance), str(number), str(operator), str(operatorref), str(errorcode), str(message), str(circle), str(network), str(user),))
        self.db.commit()

    def addSMSStatus(self,user,status,text):
        self.c.execute("INSERT INTO SMSStatus (user,status, text) VALUES (%s, %s, %s);" ,(str(user), str(status), str(text),))
        self.db.commit()

    def addReferralSMSStatus(self,user,status,text):
        self.c.execute("INSERT INTO referralSMS (user,status, text) VALUES (%s, %s, %s);" ,(str(user), str(status), str(text),))
        self.db.commit()

    def addAckRefSMS(self,user, referral, status,text):
        self.c.execute("INSERT INTO ackRefSMS (user, referral, status, text) VALUES (%s, %s, %s, %s);" ,(str(user), str(referral), str(status), str(text),))
        self.db.commit()

    def logUserTime(self,user):
        self.c.execute("UPDATE users SET lastloggedin=NOW() WHERE phone_number=%s;",(user,))
        self.db.commit()



