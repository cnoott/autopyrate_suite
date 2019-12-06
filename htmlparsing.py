from bs4 import BeautifulSoup
import requests

url = 'thepiratebay.org/search/joker'
r = requests.get("http://"+url)
data = r.text

soup = BeautifulSoup(data,"html.parser")

for link in soup.find_all("a"):
    print(link.get("href"))
#soup.find_all("p","magnet")


