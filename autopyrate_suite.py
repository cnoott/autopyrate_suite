#Written by Liam Amadio
#December 2 2019

import os
import sys
import paramiko
from bs4 import BeautifulSoup
import requests
import getpass
import time
import config #config file

#key functions

def searchtorrent(search):
    '''
    Displays searchresults from parameter and allows the user to select a torrent
    to then return magnet link
    '''
    soup = BeautifulSoup(search,"html.parser")

    title = soup.findAll("a",{"class":"detLink"})
    seeders = soup.findAll("td",{"align": "right"})
    magnet = soup.findAll("a",{"title": "Download this torrent using magnet"})
    #if thepiratebay.org is down or if no search results come back
    if title == []:
        print(config.url, "may be down or try more specific search results")
        options()
    x = 0 #varables for going through seeders/leechers list
    y = 2
    m = 0 #varable for going throgh magnets
    magnetdict = {} #for returning magnet link for repective link
    z = 1 #iterable keys for magnetdict

    for name in title:
        magnetdict[z] = magnet[m].get('href')
        sl = str(seeders[x:y])
        sl = sl.replace('<td align="right">','')#removes excess
        sl = sl.replace('</td>','')
        print("{0}. {1} | {2}".format(z,name.text,sl))
        z = z + 1
        m = m + 1
        x = x + 2
        y = y + 2
    while True:
        try:
            choice = input("Please choose a number (or type c to cancel): ")
            if (choice) == 'c':
                options()
                break
            print("Downloading",title[int(choice)-1].text)
            break
        except IndexError:
            print("Invalid option, please try again")

    return(magnetdict[int(choice)])

def autotorrent(magnet):
    '''
    Uses transmission-cli commands via ssh to start torrenting from the argument magnet file
    '''
    #getting the torrent
    torrent = "transmission-remote --auth {0}:{1} -a {2}".format(config.transmission_login,transpass,magnet)
    torrent = str(torrent)
    stdin,stdout,stderr = ssh.exec_command(torrent)
    torrentoutput = stdout.readlines()
    print("{0}!".format(torrentoutput[0][45:52]))

    #checking if torrent is done
    listtorrent = 'transmission-remote --auth {0}:{1} -l'.format(config.transmission_login,transpass)
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
    while True:
        cancelseed = input("Transmission-remote will seed for {0} minutes\nType 'c' to stop seeding now: ".format(config.seedtime/60))
        if cancelseed == 'c':
            seedtime = 0
            print('seeding canceled')
            break

    time.sleep(seedtime)
    removetorrent = 'transmission-remote --auth {0}:{1} -t all -r'.format(config.transmission_login,transpass)
    stdin,stdout,stderr = ssh.exec_command(removetorrent)
    seedoutput = stdout.readlines()
    print("{0}!".format(seedoutput[0][45:52]))

def autotransfer(choosefile, x, filelist):
    '''
    Lists files in configured directory and transfers selected file via scp
    '''
    if choosefile == "" or choosefile > x:
        print("Please choose valid number")
        autotransfer()
    chosenfile = filelist[choosefile -1].rstrip('\n')
    print("Transfering",chosenfile)
    cmd = 'scp -r {0}@{1}:{2}{3} {4}'.format(config.login,config.ip_addr,config.source_dir,chosenfile,config.dest_dir)
    os.system(cmd)

def autodelete(choosefile, x, filelist):
    '''
    Lists files in configured directory and deletes selected file
    '''
    if choosefile == "" or choosefile > x:
        print("Please choose valid number")
        autodelete()
    print("Deleting",filelist[choosefile - 1])
    stdin,stdout,stderr = ssh.exec_command("sudo rm -r /opt/plexmedia/movies/{0}".format(filelist[choosefile-1]))

def plexscan():
    '''
    Scans configured torrent download directory to update for plex
    '''
    #plex user login
    if config.plex_support == True:
        plexssh = paramiko.SSHClient()
        plexssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        plexssh.connect(hostname=config.ip_addr, username=config.plex_user,password=config.plex_pass)
        stdin,stdout,stderr = plexssh.exec_command("/usr/lib/plexmediaserver/'Plex Media Scanner' --scan --refresh --force --item 29")
        print("Updating Plex Movies library...")
        plexssh.close()

def changedirectory():
    '''
    Changes the local variable source_dir pulled from config.py
    '''
    stdin,stdout,stderr = ssh.exec_command('ls {0}'.format(config.source_dir))
    files = stdout.readlines()
    x = 1
    for filename in files:
        print(x, filename)
        x = x + 1
    choice = int(input('Choose a folder to download to/from'))
    chosen_dir = '{0}{1}'.format(config.source_dir,files[choice - 1])
    stdin,stdout,stderr = ssh.exec_command('transmission-remote --auth={0}:{1} -w {2}'.format(config.transmission_login,transpass,chosen_dir))
    return chosen_dir

#END OF KEY FUNCTIONS

#splash text
print("\nWelcome to autoPyrate v1.6\n---------------------")
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
#checking config.py if transmission password is the same as server password
if config.transmission_pass == False:
    transpass = config.transmission_password
else:
    transpass = password

def options():
    '''
    Gives the user a set of options to choose from. Changes the option variable
    '''
    option = input("Choose what you would like to do\n 1. torrent search | 2. torrent | 3. transfer | 4. delete | 5. exit\n")
    #error prevention
    if option not in ['1','2','3','4','5']:
        print("Please choose a valid number")
        options()

    if option == "1":
        search = input("Search for torrent you're looking for (or type c to cancel): ")
        if search.lower() == 'c':
            print('Canceled')
            options()
        url = config.url
        search = requests.get("{0}{1}".format(url,search))
        search = search.text
        print("Searching from",url)
        magnet = searchtorrent(search)
        changedirectory()
        autotorrent(magnet)
        plexscan()
        options()

    if option == "2":
        magnet = input("Paste magnet link here (or type c to cancel): ")
        if magnet.lower() == 'c':
            print('Canceled')
            options()
        changedirectory()
        autotorrent(magnet)
        plexscan()
        options()

    if option == "3":
        filelist = []
        chosen_dir = changedirectory()
        stdin,stdout,stderr = ssh.exec_command("ls {0}".format(chosen_dir))
        files = stdout.readlines()
        files = stdout.readlines()
        x = 1
        for i in files:
            filelist.append(i)
            print("{0}. {1}".format(x,i))
            x = x + 1
        choosefile = input("Choose file number to tansfer (or type c to cancel): ")
        if choosefile.lower() == 'c':
            print('Canceled')
            options()
        choosefile = int(choosefile)
        autotransfer(choosefile, x, filelist)
        plexscan()
        options()

    if option == '4':
        filelist = []
        chosen_dir = changedirectory()
        stdin,stdout,stderr = ssh.exec_command("ls {0}".format(chosen_dir))
        files = stdout.readlines()
        x = 1
        for i in files:
            filelist.append(i)
            print("{0}. {1}".format(x,i))
            x = x + 1
        choosefile = input("Choose file number to delete (or type c to cancel): ")
        if choosefile.lower() == 'c':
            print('Canceled')
            options()
        choosefile = int(choosefile)
        autodelete(choosefile, x, filelist)
        plexscan()
        options()

    if option == "5":
        ssh.close()
        exit()
options()
