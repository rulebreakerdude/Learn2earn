import MySQLdb
import re
from datetime import date, timedelta
from utilities import *

DB_USER = 'root'
DB_PASSWD = 'Wmtp00lr!'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'learn2earn'


class srowDatabase:
    def __init__(self, db_name=DB_NAME,db_user=DB_USER):
        db_port=DB_PORT
        db_host=DB_HOST
        db_passwd=DB_PASSWD
        self.db = MySQLdb.connect(port=db_port,host=db_host,user=db_user,passwd=db_passwd)
        self.c = self.db.cursor()
        self.c.execute('USE '+db_name+';')
        
    #SessionID Management
    
    def addHivSessionID(self,user,SessionID,datetime):
        self.c.execute("INSERT INTO hivSession (user, SessionID, datetime) VALUES (%s, %s, %s);" ,(str(user), str(SessionID), str(datetime)))
        self.db.commit()

    def getSessionID(self):
        r_SessionID = self.c.execute("SELECT DISTINCT SessionID FROM hivSession ORDER BY SessionID DESC;",)
        r_SessionID = self.c.fetchall()
        r_SessionID =[i[0] for i in r_SessionID]
        return r_SessionID[0]
		
	def updateUser