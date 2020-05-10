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
#import config #might need later

# -------- FUNCTIONS ---------
def clearscreen():
    os.system("clear")

def searchtorrent(search):
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

    query = input("Search torrent:\n>> ")
    query = "{}{}".format(searchUrl,query)

    #configures chrome driver to open as headless
    headers = "{'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'}"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920x1080")
    driver_dir = "./modifiedchromedriver"
    driver = webdriver.Chrome(options=chrome_options, executable_path=driver_dir)

    url = driver.get(query)
    if site == "1": #pirate bay search
        #driver.find_elements(By.XPATH, '//html/body/main/div[2]/section[2]/ol/li[2]/span[2]')
        soup = BeautifulSoup(url, "html.parser")
        names = soup.find_all('span',class_="list-item item-name item-title")
        for name in names:
            print(names)

        #for names in torrentNames:
        #    print(names)





def __main__():
    search = "avengers: endgame"
    searchtorrent(search)


__main__()
