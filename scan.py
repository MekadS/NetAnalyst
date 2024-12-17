#spyder 17122024 4:45pm
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

# def build_mac_vendor_map(filename):
#     mac_vendor_map = {}
#     with open(filename, "r") as f:
#         reader = csv.reader(f)
#         for row in reader:
#             if len(row) >= 2:  # Ensure the row has at least MAC and vendor columns
#                 mac_vendor_map[row[0].upper()] = row[1] 
#     #print(mac_vendor_map)
#     return mac_vendor_map


def build_mac_vendor_map(filename):
    mac_vendor_map = {}
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mac_address = row[0].upper()
                # Extract the first three octets of the MAC address
                short_mac = mac_address[:8]
                mac_vendor_map[short_mac] = row[2]
                # mac_vendor_map[short_mac] = row[1]
            
    return mac_vendor_map

def get_mac_vendor(mac_short, mac_vendor_map):
    return mac_vendor_map.get(mac_short.upper(), "Unknown")

def print_result(result_list):
    print("IP\t\t\t\t\tMAC_Address\t\t\t\t\tVendor")
    print("----------------------------------------------------------")
    for client in result_list:
        mac_short = client["mac"][:8]
        vendor = get_mac_vendor(mac_short,mac_vendor_map)
        print(f"{client['ip']}\t\t\t{client['mac']}\t\t\t{vendor}")
        
        #print(f"{client['ip']}\t\t\t{client['mac']}")



# Main function
options=get_arguments()
mac_vendor_map = build_mac_vendor_map("fTestDict.csv")
#mac_vendor_map = build_mac_vendor_map("macDict.csv")
scan_result = scan(options.ip)
print_result(scan_result)

#TESTING
# last_key, last_value = list(mac_vendor_map.items())[-1]
# print(last_key, last_value)