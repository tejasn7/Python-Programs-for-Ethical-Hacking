#!/usr/bin/env python

import SocketServer

class EchoHandler(SocketServer.BaseRequestHandler): # invoked whenever client connects
	def handle(self): #override the handle function
		print "Got connection from: ", self.client_address
		data = "dummy"
		while len(data):
			data = self.request.recv(2048) # self.request is the client socket
			print("Client sent: "+data)
			self.request.send(data)
		print("Client left")


serverAddr = ("0.0.0.0", 9000)

server = SocketServer.TCPServer(serverAddr,EchoHandler)

server.serve_forever()