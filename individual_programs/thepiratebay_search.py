from bs4 import BeautifulSoup
import requests
#url = 'thepiratebay.org/search/joker'
#r = requests.get("http://"+url)
#data = r.text

#fileHandle = open("joker.html","r")
#soup = BeautifulSoup(fileHandle,"html.parser")
#for listing titles of torrents
#title = soup.findAll("a",{"class": "detLink"})

#for listing seeders / leechers NOTE: [0:2] are both seeders and leechers for the first item
#lists both torrent name and seeders/leechers
#seeders = soup.findAll("td",{"align": "right"})
#x = 0
#y = 2
#sl = str(seeders[x:y])
#sl = sl.replace('<td align="right">','')
#sl = sl.replace('</td>','')
#for name in title:
#    print(name.text," | ",sl)
#    x = x + 2
#    y = y + 2


#lists magnet link for respective link
#magnet = soup.findAll("a",{"title": "Download this torrent using magnet"})

#print(magnet[0].get('href'))

search = input("Enter torrent you wanna look for: ")
url = 'https://thepiratebay.org/search/'
search = requests.get("{0}{1}".format(url,search))
search = search.text
def searchtorrent(search):
    '''
    Displays searchresults from parameter and allows the user to select a torrent
    to then return magnet link
    '''
    soup = BeautifulSoup(search,"html.parser")

    title = soup.findAll("a",{"class":"detLink"})
    seeders = soup.findAll("td",{"align": "right"})
    magnet = soup.findAll("a",{"title": "Download this torrent using magnet"})

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
    choice = int(input("Please choose a number: "))
    return(magnetdict[choice])


link = searchtorrent(search)
print(link)
