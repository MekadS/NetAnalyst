#spyder 17122024 4:55pm
#!/usr/bin/env python
#runfile('D:/Network_Projects/NetAnalyst/scan.py', args="-t 10.10.0.1/24", wdir='D:/Network_Projects/NetAnalyst')

import scapy.all as scapy
import csv
import argparse

#dictionary to store the registered mac addresses and their vendor names
def build_mac_vendor_map(filename):
    # mac_vendor_map = {}
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                mac_address = row[0].upper()
                # Extract the first three octets of the MAC address
                short_mac = mac_address[:8]
                mac_vendor_map[short_mac] = row[2]

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
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "vendorName": get_mac_vendor(element[1].hwsrc[:8])}
		client_list.append(client_dict)

    # print(client_list)
    # print(client_dict)
	return client_list

def get_mac_vendor(mac_short):
    return mac_vendor_map.get(mac_short.upper(), "Unknown")

def print_result(result_list):
    print(len(result_list), "devices found")
    print("IP\t\t\t\t\tMAC_Address\t\t\t\t\tVendor")
    print("-------------------------------------------------------------------------")
    for client in result_list:
        print(f"{client['ip']}\t\t\t{client['mac']}\t\t\t{client['vendorName']}")

# Main function
mac_vendor_map = {}

def beginScan(ipAddressRange):
    build_mac_vendor_map("macAddDict.csv")
    scan_result = scan(ipAddressRange)
    # print(mac_vendor_map)
        # print(answered_list)
        # print(client_list)
        # print(client_dict)
    # print(mac_vendor_map)
    # print_result(scan_result)
    return scan_result

# 1. mac_vector_map
# 2. answered_list
# 3. client_list
# 4. client_dict (TEMP)