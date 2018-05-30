

#!/usr/bin/env python
from netmiko import ConnectHandler
from getpass import getpass

#ip_addr = input("Enter IP Address: ")

device = { 
    'device_type': 'cisco_ios',
    'ip': '192.168.101.11',
    'username': 'admin',
    'use_keys': True,
    'key_file': '/home/markus/.ssh/id_rsa',
    'port': 22,
} 

print(device)
#net_connect = ConnectHandler(**device)
net_connect = ConnectHandler(device_type = 'cisco_ios', ip = '192.168.101.11', username = 'admin', use_keys = True, key_file = '/home/markus/.ssh/id_rsa', port = 22)

print (net_connect.find_prompt())
net_connect.enable()
print (net_connect.find_prompt())

output = net_connect.send_command_expect("show version")
print(output)



