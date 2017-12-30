from socket import*
from threading import Thread
import time
import select
import sys
from settings import *
def send(file_s,s,addr):
	buff=1000
	global folder
	file_name=folder+file_s
	f1=open(file_name,"rb")
	data=f1.read(buff)
	sequence=1
	#s.setblocking(0)
	timeout=5000
	
	while data:
		counter=2
		#print data
		while counter > 0:
			#time.sleep(0.001)
			s.sendto(data+"<^~^>"+str(sequence),addr)
			print ("packet %d sent"%sequence)
			pollster=select.poll()
			flag =select.POLLIN 
			pollster.register(s,flag)
			r=pollster.poll(timeout)
			if(r):
				#print "inside r"
				data,addr=s.recvfrom(buff)
				data=int(data)
				print ("receive ack of packet %d"%data)
				break
			else:
				print "timeout"
			counter-=1
		if(counter==0):
			sys.exit()
		data=f1.read(buff)
		sequence+=1
	print "sending done"
#print data
	s.sendto(data,addr)
	f1.close()
	print "done ",file_s

 
	

