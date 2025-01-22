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
                
                # Extract the required prefix of the MAC address
                if "/36" in mac_address:
                    short_mac = mac_address[:13]
                    mac_vendor_map_36[short_mac] = row[2]
                elif "/28" in mac_address:
                    short_mac = mac_address[:10]
                    mac_vendor_map_28[short_mac] = row[2]
                else:
                    short_mac = mac_address[:8]
                    mac_vendor_map[short_mac] = row[2]

# Scan the network for clients
def scan(ip):
	broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")	# Ethernet frame generation for ARP broadcast to src MAC address
	arp_request = scapy.ARP(pdst=ip) 					# ARP request generation
	arp_request_broadcast = broadcast/arp_request		# Combined the two frames for easily sending the packet
	
	# Send the packet and get the response (remember the response is in the form of a list, and those are 2 specifically - answered and unanswered ), we need to get the first element of the list so we used answered[0]
	answered_list = scapy.srp(arp_request_broadcast, timeout=2, verbose=True)[0]
    # Make verbose=False if the app gets laggy
    
	# list comprehension to get the MAC address and IP address of the client (contains nested dictionaries)
	client_list = []
	for element in answered_list:
		client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "vendorName": get_mac_vendor(element[1].hwsrc)}
		client_list.append(client_dict)

	return client_list

# After the devices MACs are found, their vendor names are obtained from the 3 dictionaries
def get_mac_vendor(mac_add):
    # Code to comb through all the 3 dictionaries containing different lengthed prefixes of the MAC addresses
    return mac_vendor_map_36.get(mac_add.upper()[:13], mac_vendor_map_28.get(mac_add.upper()[:10], mac_vendor_map.get(mac_add.upper()[:8], "Unknown")))

#For Debugging
def print_result(result_list):
    print(len(result_list), "devices found")
    print("IP\t\t\t\t\tMAC_Address\t\t\t\t\tVendor")
    print("-------------------------------------------------------------------------")
    for client in result_list:
        print(f"{client['ip']}\t\t\t{client['mac']}\t\t\t{client['vendorName']}")

# Main function
mac_vendor_map_36 = {}
mac_vendor_map_28 = {}
mac_vendor_map = {}
# build_mac_vendor_map("macAddDict.csv")

def beginScan(ipAddressRange):
    build_mac_vendor_map("macAddDict.csv")
    scan_result = scan(ipAddressRange)
    return scan_result

# 1. mac_vector_map
# 2. answered_list
# 3. client_list
# 4. client_dict (TEMP)