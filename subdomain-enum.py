import requests
import socket
import sys
from time import sleep
#from scapy.all import *

domain = sys.argv[1]
subdomains = []
final_subdomains = []
ip_list = []

f = open("subdomains.txt","r") # subdomains wordlist in subdomains.txt
for subdomain in f.readlines():
	subdomains.append(subdomain.strip())
try:
	for sub in subdomains:
		try:
			print("Trying: "+sub)
			#sleep(2)
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			host = sub+"."+domain
			s.connect((host,80))
			ip = socket.gethostbyname(host)
			#ip_list.append(ip)
			req = requests.get("http://"+host,allow_redirects=False)

			if str(req.status_code)[0] == "3":
				redirect_url = str(req.headers['Location'])
				#print(host + " - " + redirect_url + " - " + str(ip))
				if "http" in redirect_url:
					new_url = redirect_url.split("/")[2]
					#print(new_url + " - " + str(socket.gethostbyname(new_url)))
					if str(ip) == str(socket.gethostbyname(new_url)):
						#print("Same")
						if new_url in final_subdomains:
							pass
						else:

							final_subdomains.append(new_url)
					else:
						print("The subdomain " + host + " is redirected to " + redirect_url)
						#print("Different")
						if new_url in final_subdomains:
							pass
						else:
							final_subdomains.append(new_url)
				else:
					if host in final_subdomains:
						pass
					else:
						final_subdomains.append(host)
					#print(host + redirect_url)

			if str(req.status_code)[0] == "2":
				#print(host)
				if host in final_subdomains:
					pass
				else:
					final_subdomains.append(host)
			
			s.close()
		
		except: #socket.gaierror:
			pass

	for i in final_subdomains:
		print(i + " - " + socket.gethostbyname(i))
	#print("\n".join(final_subdomains))
		#print(ip_list)
except KeyboardInterrupt:
	for i in final_subdomains:
		print(i + " - " + socket.gethostbyname(i))