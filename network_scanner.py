#!/usr/bin/env python

# Algorithm
# step 1: Create ARP request directed to broadcast MAC asking for IP.
#       --> Use ARP to ask who has target IP.
#       --> Set destination MAC to broadcast MAC.
# step 2: Send the crafted packet and wait for response.
# step 3: Parse the response.
# step 4: Print result.

# To install a module in python: pip install module_name

import optparse # argparse
import scapy.all as scapy

def get_arguements():
    parser = optparse.OptionParser() # ArguementParser()
    parser.add_option("-r", "--range", dest="range", help="Range of IPs to scan") # add_arguement
    (option, args) = parser.parse_args() # argparse will return only options
    if not option.range:
        print("Enter an ip range using -r option.\n -h for help.")
        exit()
    return option


def scan(ip):
    #scapy.arping(ip)
    arp_request = scapy.ARP(pdst=ip) # Create a packet (object of class ARP) with destination ip as ip. Or arp_request.pdst=ip. Who has this particular ip? Basically this is the message. We have given a range because we want to know who has first ip, 2nd ip,3rd ip and so on. One by one each ip will be sent to the broadcast mac to be broadcasted on the network.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff") # Create a broadcast frame. Create an ethernet object. Broadcast MAC address. It is virtual but when you send something to it, all devices will recieve it. Since in a lan communication takes place by mac and not ip. This is the mac to whom to send the above message to.
    arp_request_broadcast = broadcast/arp_request # Combine the above two packets. Packet will go to broadcast mac ff:ff:ff:ff:ff:ff asking who has ip pdst.
    # answered_list, unanswered_list = scapy.srp(arp_request_broadcast, timeout=1) # scapy.sr->send recieve scapy.srp-> send recieve packets that have a custom ether part. It will return 2 lists(i.e. arrays) for answered and unanswered.
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0] # Will return only the answered ones. Only first list.
    client_list = []
    for element in answered_list:
        client_dict = {"ip":element[1].psrc,"mac":element[1].hwsrc}
        client_list.append(client_dict)
        #print(element[1].psrc+"\t\t\t"+element[1].hwsrc) # Each element is a list in itself, [0] is the request and [1] is the answer.
        #print(element[1].hwsrc) # Each element is a list in itself, [0] is the request and [1] is the answer.
    return (client_list)
    # arp_request.show()
    # broadcast.show()
    # arp_request_broadcast.show() # More detailed description.
    #print(arp_request.summary()) # What the packet is doing.
    # scapy.ls(scapy.ARP()) # Give info of all variables to set for class ARP. Can also be used for Ether class.

def print_result(result_list):
    print("IP\t\t\t\tMAC Address\n-------------------------------------------------")
    for client in result_list:
        print(client["ip"]+"\t\t\t"+client["mac"])
option = get_arguements()
scan_list = scan(option.range)
print_result(scan_list)
