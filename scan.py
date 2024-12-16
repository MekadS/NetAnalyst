
#!/usr/bin/env python
#runfile('D:/Network_Projects/NetAnalyst/scan.py', args="-t 10.10.0.1/24", wdir='D:/Network_Projects/NetAnalyst')

import scapy.all as scapy
import csv
import argparse

# Get the arguments from the command line
def get_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--target", dest="ip", help="Enter IP address or IP address range of target network")
	options = parser.parse_args()
	if not options.ip:
		parser.error("[-] Please specify an IP address or IP address range, use --help for more info")

	return options

# Scan the network for clients
def scan(ip):
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")	# Ethernet frame generation for ARP broadcast to src MAC address
	arp_request = scapy.ARP(pdst=ip) 					# ARP request generation
	arp_request_broadcast = broadcast/arp_request		# Combined the two frames for easily sending the packet
	
	# Send the packet and get the response (remember the response is in the form of a list, and those are 2 specifically - answered and unanswered ), we need to get the first element of the list so we used answered[0]
	answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]
	
	# list comprehension to get the MAC address and IP address of the client (contains nested dictionaries)
	client_list = []
	for element in answered_list:
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
		client_list.append(client_dict)
	return client_list

def get_mac_vendor(mac_address):
    with open("macDict.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row[0].upper() == mac_address.upper(): 
                return row[1]
    return "Unknown"

def print_result(result_list):
    """
    Prints the IP address, MAC address, and vendor name for each device.
    """
    print("IP\t\t\t\tMAC_Address\t\t\tVendor")
    print("----------------------------------------------------------")
    for client in result_list:
        vendor = get_mac_vendor(client["mac"])
        print(f"{client['ip']}\t\t\t{client['mac']}\t\t\t{vendor}")



# Main function
options=get_arguments()
scan_result = scan(options.ip)
print_result(scan_result)