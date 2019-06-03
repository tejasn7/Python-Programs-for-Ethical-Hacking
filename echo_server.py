#!/usr/bin/env python

import socket

tcpSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
tcpSocket.bind(("0.0.0.0",8000))
tcpSocket.listen(2)

(client,(ip,port)) = tcpSocket.accept()
client.send("Welcome to echo server. Type exit to quit\n\n")
print("Client connected.\n\n")
data = ""

while "exit" not in data:
	data = client.recv(1024)
	print("Client sent: "+data)
	client.send("Server says: "+data)

client.close()
tcpSocket.close()