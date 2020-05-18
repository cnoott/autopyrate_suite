#Written by Liam Amadio
#Created December 2 2019, Updated May 5 2020

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

import os
import sys
import paramiko
from bs4 import BeautifulSoup
import getpass
import time
import config #might need later

# -------- FUNCTIONS ---------
def clearscreen():
    os.system("clear")

def searchtorrent():
    '''
    prompts user to choose torrent site and prints a list of torrents of their search. Returns magent link.
    '''
    while True:
        site = input("1.PirateBay\n2.RARBG\nChoose a site to search from: ")
        if site == "1":
            searchUrl = "https://thepiratebay.org/search.php?q="
            break
        elif site == "2":
            searchUrl = "https://www.rarbg.to/torrents.php?search="
            break
        else:
            print("invalid option")

    printlogo()
    query = input("Search torrent:\n>> ")
    query = "{}{}".format(searchUrl,query)

    #configures chrome driver to open as headless
    headers = "{'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver_dir = "./modifiedchromedriver"
    driver = webdriver.Chrome(options=chrome_options, executable_path=driver_dir)

    #get page
    driver.get(query)
    html = driver.page_source

    #pirate bay search
    if site == "1":
        soup = BeautifulSoup(html, "html.parser")

        #finds names, seeders, leechers, and magnetlinks
        names = soup.find_all('span',class_="list-item item-name item-title")
        seeders = soup.find_all ('span', class_="list-item item-seed")
        leechers = soup.find_all('span', class_="list-item item-leech")
        magnetlinks = soup.select("a[href*=magnet]")
        count = 1
        for name, seeder, leecher in zip(names[:10], seeders[:10], leechers[:10]):
            childName = name.findChild("a", recusrive=False)
            print("{}. {}   [{}:{}]".format(count,childName.text, seeder.text, leecher.text))
            count += 1

        #choose torrent
        while True:
            option = int(input("Choose an option: "))
            if option in range(1,11):
                printlogo()
                magnet = magnetlinks[option-1]
                magnet = magnet.get('href')
                print(magnet)
                return magnet
            else:
                print("invalid option")


def autotorrent(magnet):
    '''
    Uses transmission-cli commands via ssh to start torrenting from the argument magnet file
    '''
    #getting the torrent
    torrent = r"transmission-remote --auth {0}:{1} -a '{2}'".format(config.transmission_login,transpass,magnet)
    torrent = str(torrent)
    stdin,stdout,stderr = ssh.exec_command(torrent)
    torrentoutput = stdout.readlines()
    try:
        print("{0}!".format(torrentoutput[0][45:52]))
    except IndexError:
        print(torrentoutput)

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
    print("Updating Plex movies library")
    if config.plex_support == True:
        plexssh = paramiko.SSHClient()
        plexssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        plexssh.connect(hostname=config.ip_addr, username=config.plex_user,password=config.plex_pass)
        stdin,stdout,stderr = plexssh.exec_command("/usr/lib/plexmediaserver/'Plex Media Scanner' --scan --refresh --force --item 29")
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
    printlogo()
    return chosen_dir
def activatevpn():
    '''
    activates vpn via openvpn command via ssh
    '''
    stdin,stdout,stderr = ssh.exec_command('sudo openvpn /home/pi/pimedia.ovpn')


def printlogo():
    clearscreen()
    logo = '''
          ____
        ,'   Y`.
       /        \

       \ ()  () /
        `. /\ ,'
    8====| "" |====8
         `LLLU'
    '''
    print(logo,"\033[1;32;40m \n-= Welcome to autoPyrate v2.0 =-\n\033[0m")

#--------- CODE ---------

printlogo()
if config.ip_addr == "":
    print("No ip_addr provided in config file")
    exit()
print("Please login to your configured server")

#ssh login
while True:
    user = input("Ente server username here: " )
    password = getpass.getpass(prompt="Enter server password: ")
    print("connetcing to {}@{}".format(user,config.ip_addr))
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=config.ip_addr, username=user, password=password)
        print("Connected!")
        time.sleep(1)
        printlogo()
        break
    except paramiko.AuthenticationException:
        print("Authentication failed")

#checking config.py if tranmission password is the same as server password
if config.transmission_pass == False:
    transpass = config.transmission_password
else:
    transpass = password

#options
while True:
    option = input("Choose what you would like to do\n 1. torrent search | 2. torrent | 3. Turn on VPN | 4. delete | 5. exit\n")
    if option == "1":
        magnet = searchtorrent()
        changedirectory()
        autotorrent(magnet)
        plexscan()

    elif option == "2":
        magnet = input("Paste magnet link here:")
        changedirectory()
        autotorrent(magnet)
        plexscan()
        options()

    elif option == "3":
        activatevpn()

    elif option == "4":
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
    elif option == "5":
        ssh.close()
        exit()
    else:
        print("Invalid option")



