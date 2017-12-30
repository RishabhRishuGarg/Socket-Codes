import sys
from socket import*
from settings import*
import os
import time
from threading import Thread
from fullreceive import receive
from fullreceive import send
from subprocess import check_output

my_files= check_output('ls'+' '+folder,shell=True) # this function will send the output of given LINUX command in argument ,,ls command return the files and folder in given path

list_file=my_files.split("\n") # check_output function return the string with file name seprated by "\n" to get the list of file string should to be split by "\n"
list_file.remove("") # removing blank spaces from list
#print list_file
new_files=[]
print "My system files are :"+"\n",my_files
folder=folder+"/"
s=socket(AF_INET,SOCK_DGRAM) # Creating Socket
addr=(host,port)
#s.bind(addr)
buff=1024
s.sendto(my_files,addr) # Sending the files of this system directory
server_files,server_addr=s.recvfrom(buff) # receiving the files of server directory
#print server_files,server_addr
server_files=server_files.split('\n') 
server_files.remove("")
str_files=""
x=0
for file_s in server_files: # this loop is to control the common files and missing files in directory
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
requi_file,server_addr=s.recvfrom(buff)  # receiving the files required by the server
print "Files required by the server are \n",requi_file
print "server address is ",server_addr
requi_file=requi_file.split(",")
s.sendto(str_files,server_addr) # sending the list of files required by this machine
#print str_files
#time.sleep(0.1)
def receive_files(): # this loop handle the receiving of all files one by one
	global new_files
	global s
	for file_s in new_files:
		if file_s=="":
			continue
		print "receiving ",file_s
		receive(file_s)
#time.sleep(1)
def send_files(arg): # this loop handle the sending of all files one by one
	global requi_file
	global s
	global server_addr
	for file_s in requi_file:
		if file_s=="":
			continue
		print "Sending ",file_s
		send(file_s,server_addr)
thread1=Thread(target=send_files,args=("thread",)) # creating the thread of sending for FULL duplex exvironment
thread1.start()
receive_files()
thread1.join()
s.close()
