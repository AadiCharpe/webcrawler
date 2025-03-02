import time
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
# starting urls
urls = ['https://www.wikipedia.org/', 'https://www.cnn.com/']

visited = []
number = 3
# number > 0 is just because I am testing
while urls and number > 0:
    url = urls.pop()
    print('crawling: ' + url)
    canVisit = True
    response = requests.get('https://' + urlparse(url).netloc + '/robots.txt')
    disallowed = []
    for line in response.text.splitlines():
        if line.startswith('Disallow') and len(line.split()) > 1:
            disallowed.append(line.split()[1])
    for path in disallowed:
        if urlparse(url).path.startswith(path):
            canVisit = False
            break
    if not canVisit:
        print('cant crawl ' + url + ' because of robots.txt')
        continue
    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    for link in soup.find_all('a'):
        if link.get('href').startswith('//'):
            if 'https:' + link.get('href') not in visited:
                urls.append('https:' + link.get('href'))
        elif link.get('href').startswith('http'):
            if link.get('href') not in visited:
                urls.append(link.get('href'))
    visited.append(url)
    number -= 1
    time.sleep(1.5)
print(visited)
