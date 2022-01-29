import paramiko
import time

host = '158.101.210.158'
port = '22'
user = 'ubuntu'

session = paramiko.SSHClient()
session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

key_file = paramiko.RSAKey.from_private_key_file(r"C:\Users\akeel\OneDrive\Glassolega\glassolega_ssh_rsa")
session.connect(
	hostname = host,
	port=port,
	username = user,
	pkey=key_file
	)

stdin, stdout, stderr = session.exec_command('cd /home/ubuntu/glassolega_bot/Glassolega;\
                                              sudo systemctl stop glassolega.service;\
                                              git pull https://github.com/akeelow/Glassolega.git;\
                                              sudo systemctl start glassolega.service;\
                                              sudo systemctl status glassolega.service\
                                              ')
time.sleep(.5)

print(stdout.read().decode())
session.close()