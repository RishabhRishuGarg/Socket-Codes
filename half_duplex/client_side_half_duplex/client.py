import sys
from socket import*
from settings import*
import os
import time
from halfreceive import receive
from halfsend import send
from subprocess import check_output
my_files= check_output('ls'+' '+folder,shell=True)

list_file=my_files.split("\n")
list_file.remove("")
#print list_file
new_files=[]
print "My system files are :"+"\n",my_files
folder=folder+"/"
s=socket(AF_INET,SOCK_DGRAM)
addr=(host,port)
#s.bind(addr)
buff=1024
s.sendto(my_files,addr)
server_files,server_addr=s.recvfrom(buff)
#print server_files,server_addr
server_files=server_files.split('\n')
server_files.remove("")
str_files=""
x=0
for file_s in server_files:
	if(file_s in list_file):
		i=0
	else:
		if x==0:
			str_files=file_s
			x+=1
		else:
			str_files=str_files+","+file_s
		new_files.append(str(file_s))
print "Files required to this machine ; \n",new_files
requi_file,server_addr=s.recvfrom(buff)
print "Files required by the server are \n",requi_file
print "server address is ",server_addr
requi_file=requi_file.split(",")
s.sendto(str_files,server_addr)
#print str_files
time.sleep(0.1)
for file_s in requi_file:
	if file_s=="":
		continue
	print "Sending ",file_s
	send(file_s,s,server_addr)
#s=socket(AF_INET,SOCK_DGRAM)
#addr=(host,port) 
for file_s in new_files:
	if file_s=="":
		continue
	print "receiving ",file_s
	receive(file_s,s)
s.close()

