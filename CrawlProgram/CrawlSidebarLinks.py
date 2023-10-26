from bs4 import BeautifulSoup
import json
import requests

r = requests.get('https://matplotlib.org/stable/api/index.html')  # Demo网址
demo = r.text

gallery_link = []
soup = BeautifulSoup(demo, "html.parser")
element = soup.select('div.bd-toc-item.navbar-nav a.reference.internal')
# headings = element.find_all(['a'])
for heading in element:
    href = heading.get('href')
    if href:
        gallery_link.append({'url': "https://matplotlib.org/stable/api/" + href})

with open('../crawled_links/crawled_api_reference_links.json', 'w') as json_file:
    json.dump(gallery_link, json_file, indent=4)
