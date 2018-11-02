import wave
import sys
import os
from pydub import AudioSegment

def chk_call(file1):

	file1 = file1.split("/")[0]
	base_loc = "home/navneet/web/loudblog/";
	loc1 = base_loc+"audio/"+file1;
	file2 = file1.split(".")[0];
	file2 = file2+".wav";
	loc2 =  base_loc+"wave/"+file2;

	sound = AudioSegment.from_mp3(loc1);
	sound.export(loc2,format="wav");
	c1 = 0
	c2 = 0
	duration = 0
	ip = wave.open(loc2,'r');
	frames = ip.getnframes()
	rate = ip.getframerate()
	duration = frames / float(rate)

	print "starting loop";
	for i in range(ip.getnframes()):
		iframes = ip.readframes(1)
		amp = int(iframes.encode('hex'),16)
		if(amp<3000):
			c1 = c1+1
		else:
			c2 = c2+1

	tot = c1+c2;
	print "loop over";
	res1 = float(c1)/float(tot)*100;
	res = res1/duration;
	set1 = -1
	if res<0.22:
		set1 = 1
	else:
		set1 = 0
	os.remove(loc2);
	ip.close();
	print "just before return";
	return set1;
