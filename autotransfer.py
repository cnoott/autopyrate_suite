#Written by Liam Amadio
#December 1 2019

import os
import sys
import paramiko
import getpass
import config #config file

#ssh login
while True:
    user = input("Enter server username here: ")
    password = getpass.getpass(prompt="Enter server password: ")
    print("Connecting to {0}@{1}".format(user,config.ip_addr))
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=config.ip_addr,username=user,password=password)
        print("Connected!")
        break
    except paramiko.AuthenticationException:
        print("Authentication failed")

filelist = []
stdin,stdout,stderr = ssh.exec_command("ls /opt/plexmedia/movies")
files = stdout.readlines()
x = 1
for i in files:
    filelist.append(i)
    print("{0}. {1}".format(x,i))
    x = x + 1

choosefile = int(input("Choose file number to tansfer: "))
chosenfile = filelist[choosefile -1]
print("Transfering",chosenfile)
cmd = 'scp -r {0}@{1}:{2}/{3} {4}'.format(config.login,config.ip_addr,config.source_dir,chosenfile,config.dest_dir)
print(cmd)
os.system(cmd)
ssh.close()
