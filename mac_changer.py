#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguements():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface whose MAC to change")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC Address ")
    (options, arguements) = parser.parse_args()
    if not options.interface:
        parser.error("[-] Please enter the interface. Use --help for help menu.")
    elif not options.new_mac:
        parser.error("[-] Please enter the new mac. Use --help for help menu.")
    return options

def change_mac(interface,new_mac):
    print("[+] Changing mac address of interface " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])  # more secure as the value of variable cannot be hijacked.
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_search_result:
        return mac_search_result.group(0)
        # print(mac_search_result.group(0))
    else:
        print("[-] This interface does not have a mac address")

options = get_arguements()
mac = get_current_mac(options.interface)
print("[+] Current MAC is "+str(mac))
change_mac(options.interface,options.new_mac)
mac = get_current_mac(options.interface)
if mac == options.new_mac:
    print("[+] MAC has been successfully updated to "+mac)
else:
    print("[-] Failed to update MAC")



#options = get_arguements()
# change_mac(options.interface,options.new_mac)
# if mac_search_result == options.new_mac:
#     print("[+] MAC changed successfully")
# else:
#     print("[-] Could not change MAC")
#interface=raw_input("[+] Enter interface to change mac for > ")
#new_mac=raw_input("[+] Enter new mac > ")
# subprocess.call("ifconfig "+interface+" down", shell=True)
# subprocess.call("ifconfig "+interface+" hw ether "+new_mac, shell=True)
# subprocess.call("ifconfig "+interface+" up", shell=True)

