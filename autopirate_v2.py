#Created by Liam Amadio
#November 17, 2019
#This program is designed to automatically torrent and transfer a torrented file from server to this machine.

import os
import sys
import paramiko

#Config
ip_addr ='173.224.111.159'
source_dir = '/opt/plexmedia/movies/'
dest_dir = '~/Downloads'
login = 'pi'

#Splash text
print("Welcome to autoPirate_V2 \n=======================")

#ssh login
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ip_addr, username=login, password='pizzamasterrace4')
t = ssh_client.get_transport()
chan = t.open_session()
chan.request_x11()

#function for reading output of ssh
def readssh(stdout):
   output = stdout.readlines()
   print(output) #maybe change to return later?

#Getting the torrent
magnet = input("Paste magnet link here: ")
torrent = str("transmission-remote -a {0}".format(magnet))
stdin,stdout,stderr = chan.exec_command(torrent)
stdin,stdout,stderr = ssh_client.exec_command("transmission -l") #for certain things you need to use ssh_client. instead of chan.
print(stdout)
readssh(stdout)
#Detecting if download is done
#input = "transmission-remote -l"
#stdin,stdout,stderr = chan.exec_command(input)
#outputlist = readssh(stdout)
#print(outputlist)

#file_name = input('Enter exact filename here (rename and or paste from transmission client')

#cmd = 'scp -r {0}@{1}:{2}{3} {4}'.format(login,ip_addr,source_dir,file_name,dest_dir)
#os.system(cmd)

chan.close()
