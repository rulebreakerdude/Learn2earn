import db_interact as di
import datetime
while 'My name is Naagu' != 'Snake':
	z=datetime.datetime.now()
	y=z+datetime.timedelta(seconds = 57)
	if z.minute%3==0 and y.minute%3==0:
		di.fake_cron()	
		