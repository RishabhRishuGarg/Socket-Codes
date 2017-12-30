import sys
from threading import Thread
from socket import*
from settings import*
import time
import os
from fullreceive import receive
from fullreceive import send
from datetime import datetime
#from halfsend import send
from subprocess import check_output
start_time=datetime.now() # taking stating time of execution of code

my_files= check_output('ls'+' '+folder,shell=True) # this function will send the output of given LINUX command in argument ,,ls command return the files and folder in given path
new_files=[]	# creating the array
list_file=my_files.split("\n") # check_output function return the string with file name seprated by "\n" to get the list of file string should to be split by "\n"
list_file.remove("")	# removing blank spaces from list
print "My system files are"+"\n",list_file

#print my_files
folder=folder+"/"
s=socket(AF_INET,SOCK_DGRAM) # Creating Socket
addr=(host,port)	
s.bind(addr)	# create the server in given address(addr)
buff=1024
client_files,cli_addr=s.recvfrom(buff) # this recv is used for listening the client request
#print client_files,cli_addr
client_files=client_files.split('\n')	# this function will split the string into list by "\n"
client_files.remove("")		# removes blank spaces
s.sendto(my_files,cli_addr)	# sending its directory files to the client
str_files=""
x=0
for file_s in client_files: # this loop is for checking the common file 
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
s.sendto(str_files,cli_addr) # sending the list of file which are required by this machine
requi_file,cli_addr=s.recvfrom(buff) # receiving the files which are required by the client
requi_file=requi_file.split(",")
print "files required by the clients are: ",requi_file
print "clinet address is",cli_addr
def receive_files():	# this function handle's the receiving of every file one by one 
	global new_files
	global s
	for file_s in new_files:
		if file_s=="":
			continue
		print "receiving ",file_s
		receive(file_s)
#time.sleep(1)
def send_files(arg): # this function handle the sending of all files one by one
	print "Called send Function: "
	global requi_file
	global s
	global cli_addr
	for file_s in requi_file:
		if file_s=="":
			continue
		print "Sending ",file_s
		send(file_s,cli_addr) 

thread1=Thread(target=send_files,args=("thread",)) # creating the thread for handling the sending of files so that sending and receiving can be done simultaneously
thread1.start() 
receive_files()
thread1.join()	# wait for the thread to complete its execution 
s.close()
end_time=datetime.now()
print "Time take by the code to run is :- ",(end_time-start_time).total_seconds()
