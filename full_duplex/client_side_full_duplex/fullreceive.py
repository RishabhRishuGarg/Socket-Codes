from socket import*
from threading import Thread
import time
import select
import sys
from settings import*

def receive(file_name):
	#print "start"+arg
	s=socket(AF_INET,SOCK_DGRAM)
	sequence=[]
	host='127.0.0.1'
	port=7000
	addr=(host,port)
	
	s.bind(addr)
	buff=1030
	data,addr=s.recvfrom(buff)
	#print data
	counter=1
	f1=open(folder+file_name,"wb")
	while data:
		data,value=data.split("<^~^>")
		value=int(value)
		if value not in sequence:
			f1.write(data)
			sequence.append(value)
		#if(counter==5):
		#	time.sleep(6)
		#time.sleep(0.00000001)
		s.sendto(str(value),addr)
		print ("receive packet %d"%value)
		data,addr=s.recvfrom(buff)
		#print data
		counter+=1
		
	
	print "totally received file"
	f1.close()
	s.close()
	print "done"

def send(file_name,addr):
	print "------------------------------------- Called Send function---------------------------------------"
	global folder
#	time.sleep(0.00000001)
	#time.sleep(5)
	#print "start"+arg
	s=socket(AF_INET,SOCK_DGRAM)
	host='127.0.0.1'
	port=6000
	buff=1000
	addr=(host,port)
	f1=open(folder+file_name,"rb")
	data=f1.read(buff)
	sequence=1
	s.setblocking(0)
	timeout=5000

	while data:
		counter=2
		#print data
		while counter > 0:
			#print "true"
			#print ("c=%d" %counter)
			#time.sleep(0.001)
			s.sendto(data+"<^~^>"+str(sequence),addr)
			print ("packet %d sent"%sequence)
			pollster=select.poll()
			flag =select.POLLIN 
			pollster.register(s,flag)
			r=pollster.poll(timeout)
			if(r):
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
	
