#Written by Liam Amadio
#December 2 2019

import os
import sys
import paramiko
import getpass
import time
import config #config file

#splash text
print("\nWelcome to autoPyrate v0.2\n---------------------")
#error prevention
if config.ip_addr == "":
    print("No ip_addr provided in config file")
    exit()
print("Please login to your configured server")

#ssh login
while True:
    user = input("Enter server username here: ")
    password = getpass.getpass(prompt="Enter server password: ")
    print("Connecting to {0}@{1}".format(user,config.ip_addr))
    try:
        ssh=paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=config.ip_addr, username=user, password=password)
        print("Connected!")
        break
    except paramiko.AuthenticationException:
        print("Authentication failed")

def options():
    option = input("Choose what you would like to do\n 1. torrent | 2. transfer | 3. delete | 4. exit\n")
    if option == "1":
        def autotorrent():
            #getting the torrent
            magnet = input("Paste magnet link here: ")
            #if blank input
            if magnet == "":
                autotorrent()
            torrent = "transmission-remote --auth {0}:{1} -a {2}".format(config.transmission_login,password,magnet)
            torrent = str(torrent)
            stdin,stdout,stderr = ssh.exec_command(torrent)
            torrentoutput = stdout.readlines()
            print("{0}!".format(torrentoutput[0][45:52]))

            #checking if torrent is done
            listtorrent = 'transmission-remote --auth {0}:{1} -l'.format(config.transmission_login,password)
            stdin,stdout,stderr = ssh.exec_command(listtorrent)
            status = stdout.readlines()
            #checks if download is done every 30 seconds
            starttime = time.time()
            while True:
                stdin,stdout,stderr = ssh.exec_command(listtorrent)
                status = stdout.readlines()
                status = status[1][7:10]
                sys.stdout.write('\r Progress {0}%'.format(status))
                if status == '100':
                    print("\nDownload complete!")
                    break
                time.sleep(30.0 - ((time.time() -starttime) %30.0))

            #deleting torrent file after seeding for configured minutes (default 10)
            seedtime = config.seedtime
            calculatedseedtime = "Transmission-remote will seed for",config.seedtime / 60,"minutes\nType 'c' to stop seeding now"
            cancelseed = input("Transmission-remote will seed for {0} minutes\nType 'c' to stop seeding now: ".format(config.seedtime/60))
            if cancelseed == 'c':
                seedtime = 0
            time.sleep(seedtime)
            removetorrent = 'transmission-remote --auth {0}:{1} -t all -r'.format(config.transmission_login,password)
            stdin,stdout,stderr = ssh.exec_command(removetorrent)
            seedoutput = stdout.readlines()
            print("{0}!".format(seedoutput[0][45:52]))
            options()
        autotorrent()
    if option == '2':
        filelist = []
        stdin,stdout,stderr = ssh.exec_command("ls /opt/plexmedia/movies")
        files = stdout.readlines()
        x = 1
        for i in files:
            filelist.append(i)
            print("{0}. {1}".format(x,i))
            x = x + 1
        def autotransfer():
            choosefile = int(input("Choose file number to tansfer: "))
            if choosefile == "" or choosefile > x:
                print("Please choose valid number")
                autotransfer()
            chosenfile = filelist[choosefile -1].rstrip('\n')
            print("Transfering",chosenfile)
            cmd = 'scp -r {0}@{1}:{2}{3} {4}'.format(config.login,config.ip_addr,config.source_dir,chosenfile,config.dest_dir)
            os.system(cmd)
            options()
        autotransfer()

    if option == '3':
        filelist = []
        stdin,stdout,stderr = ssh.exec_command("ls /opt/plexmedia/movies")
        files = stdout.readlines()
        x = 1
        for i in files:
            filelist.append(i)
            print("{0}. {1}".format(x,i))
            x = x + 1
        def autodelete():
            choosefile = int(input("Choose file number to delete: "))
            if choosefile == "" or choosefile > x:
                print("Please choose valid number")
                autodelte()
            print("Deleting",filelist[choosefile - 1])
            stdin,stdout,stderr = ssh.exec_command("sudo rm -r /opt/plexmedia/movies/{0}".format(filelist[choosefile-1]))
            options()
        autodelete()

    if option == '4':
        ssh.close()
options()
