import paramiko
import time

time.sleep(1)

#ip="192.168.101.11"
ip="192.168.0.1"
host=ip
username = "admin"
password = "cisco123"

k = paramiko.RSAKey.from_private_key_file("/home/markus/.ssh/id_rsa")


remote_conn_pre = paramiko.SSHClient()
remote_conn_pre
remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy())
remote_conn_pre.load_system_host_keys()
#remote_conn_pre.connect(ip, username=username, pkey=k, look_for_keys=True, allow_agent=True)
remote_conn_pre.connect(ip, username=username, pkey=k)
#remote_conn_pre.connect(ip, username=username, key_filename='/home/markus/.ssh/id_rsa.pem', look_for_keys=False, allow_agent=False)
#remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
print("SSH connection established to " + host)
    
remote_conn = remote_conn_pre.invoke_shell()
print("Interactive SSH session established")

output = remote_conn.recv(1000)
print(output)   

remote_conn.send("\n")
remote_conn.send("utils system restart\n")
time.sleep(5)

output = remote_conn.recv(5000)
print(output)



