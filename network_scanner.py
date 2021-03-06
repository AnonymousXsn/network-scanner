import scapy.all as scapy
import requests
import time
import os
import table


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        mac_list = [element[1].hwsrc]
        for address in mac_list:

            vendor = requests.get('http://api.macvendors.com/' + address).text
            time.sleep(1)
            client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc, "mac_vendor": vendor if str(vendor) != '{"errors":{"detail":"Not Found"}}' else "Unknown Vendor"}
            client_list.append(client_dict)
    return client_list


def result(result_list):
    a_lst = []
    for client in result_list:
        lst = []
        lst.append(client["ip"])
        lst.append(client["mac"])
        lst.append(client["mac_vendor"])
        a_lst.append(lst)
    labels = ["IP", "MAC Address", "MAC Vendor"]
    a = table.make_table(rows=a_lst, labels=labels, centered=True)
    print(a)

if os.geteuid() != 0:
    print("You need root privileges to run this script!")
    
else:
    ip_address = input("Enter the ip address and range that you want to scan(ex: 192.168.1.1/24): ")
    scan_result = scan(ip_address)
    result(scan_result)

