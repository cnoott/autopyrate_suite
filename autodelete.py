#Written by Liam Amadio
#December 1, 2019
#This program is made to easily view and delete files from the /opt/plexmedia/movies directory
import os
import sys
import paramiko

#Config
ip_addr = '173.224.111.159'
source_dir = '/opt/plexmedia/movies/'
login = 'pi'

#ssh login
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_addr, username=login, password='pizzamasterrace4')

#function for reading output of ssh and stores it in dictionary
def readssh(stdout):
    moviedict = {}
    output = stdout.readlines()
    
    x = 1
    for i in output:
        moviedict.update(x = i)
        out = str("{0}. {1}".format(x,i))
        print(out)
        x = x + 1
    print(moviedict)


stdin,stdout,stderr = ssh_client.exec_command("ls /opt/plexmedia/movies")
readssh(stdout)
