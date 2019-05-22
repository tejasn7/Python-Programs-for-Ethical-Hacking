#!/usr/bin/env python

import scapy.all as scapy
import optparse

def get_hosts(ip):
	arp=scapy.ARP(pdst=ip)
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
	pack = broadcast/arp
	answer = scapy.srp(pack, timeout=2, retry=2)[0]
	x=0
	host_list = []
	for x in answer:
		host_list.append(x[1].psrc)
	return host_list

def scan_ports(ip):
	port_list = []
	i=1
	while i<1025:
		port_list.append(i)
		i=i+1
	port_list.append(2121)
	packet = scapy.IP(dst=ip)/scapy.TCP(dport=port_list)
	ans,unans=scapy.sr(packet, timeout=2)
	yes=0
	if ans:
		print("Result for "+ip)
		for j in ans:
			if str(j[1][scapy.TCP].flags) == "SA":
				yes=1
				print("Port: "+str(j[1][scapy.TCP].sport)+" is open")
		if yes==0:
			print("Common ports are closed on this host")


parser = optparse.OptionParser()
parser.add_option("-i","--ip",dest="ip",help="IP to scan")
(option,args)=parser.parse_args()
if not option.ip:
	print("Enter ip using -i or --ip arguement")
	exit(0)
list_of_ip = get_hosts(option.ip)
for ip in list_of_ip:
	scan_ports(ip)
	
