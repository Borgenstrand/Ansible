
from netmiko import ConnectHandler
device = ConnectHandler(device_type='cisco_ios', ip='192.168.101.11',username='admin',password='cisco123',secret='cisco123')
SendingCommands=["username Markus secret cisco123"]

print (device.find_prompt())
device.enable()
print (device.find_prompt())
device.config_mode()
print (device.find_prompt())

output=device.send_config_set(SendingCommands)
print(output)


device.disconnect()
