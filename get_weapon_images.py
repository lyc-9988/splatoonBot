# modified from https://stackoverflow.com/questions/18408307/how-to-extract-and-download-all-images-from-a-website-using-beautifulsoup

import re
import requests
from bs4 import BeautifulSoup
import os

site = 'https://www.splatoonwiki.org/wiki/Category:Weapon_icons_in_Splatoon_2'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
weaponUl = soup.find("ul", {"class": "gallery mw-gallery-traditional"})
img_tags = weaponUl.find_all('img')
icon_dir_path = "resources/weaponIcons/"

if not os.path.exists(icon_dir_path):
    os.makedirs(icon_dir_path)

for img in img_tags:
    url = img['src']
    name = img['alt']
    filename = re.search(r'/((120px)[\w\.%_-]+(.png))$', url)
    # TODO exclude salmon run weapons
    if not filename:
         print("Regex didn't match with the url: {}".format(url))
         continue
    icon_path = "resources/weaponIcons/" + filename.group(1)
    with open(icon_path, 'wb') as f:
        if 'http' not in url:
            url = 'https:{}'.format(url)
        print("downloading from url: " + url)
        response = requests.get(url)
        f.write(response.content)
