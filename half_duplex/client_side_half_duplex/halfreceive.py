from socket import*
from threading import Thread
import time
from settings import *
def receive(file_s,s):
	buff=1024
	sequence=[]
	global folder
	data,addr=s.recvfrom(buff)
	#print data
	counter=1
	f1=open(folder+file_s,"wb")
	while data:
		try:
			data,value=data.split("<^~^>")
		except:
			continue
		value=int(value)
		if value not in sequence:
			f1.write(data)
			sequence.append(value)
		#time.sleep(0.001)
		s.sendto(str(value),addr)
		print ("receive packet %d"%value)
		data,addr=s.recvfrom(buff)
		#print data
		counter+=1
		
		
	print "totally received file"
	f1.close()
	print "done"
	
	
