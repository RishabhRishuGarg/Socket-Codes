import sys
from socket import*
from settings import*
import time
from datetime import datetime
import os
from halfreceive import receive
from halfsend import send
from subprocess import check_output
start=datetime.now()
my_files= check_output('ls'+' '+folder,shell=True)
new_files=[]
list_file=my_files.split("\n")
list_file.remove("")
print "My system files are"+"\n",list_file
#print my_files
folder=folder+"/"
s=socket(AF_INET,SOCK_DGRAM)
addr=(host,port)
s.bind(addr)
buff=1024
client_files,cli_addr=s.recvfrom(buff)
#print client_files,cli_addr
client_files=client_files.split('\n')
client_files.remove("")
s.sendto(my_files,cli_addr)
str_files=""
x=0
for file_s in client_files:
	if(file_s in list_file):
		i=0
	else:
		if(x==0):
			str_files=file_s
			x+=1
		else:
			str_files=str_files+","+file_s	
		new_files.append(file_s)
print "files Required to this machine :\n",new_files
s.sendto(str_files,cli_addr)
requi_file,cli_addr=s.recvfrom(buff)
requi_file=requi_file.split(",")
print "files required by the clients are: ",requi_file
print "clinet address is",cli_addr
for file_s in new_files:
	if file_s=="":
		continue
	print "receiving ",file_s
	receive(file_s,s)
#time.sleep(20)
for file_s in requi_file:
	if file_s=="":
		continue
	print "Sending ",file_s
	send(file_s,s,cli_addr) 


s.close()
end=datetime.now()
print "Total taken by the program to execute ",(end-start).total_seconds()
