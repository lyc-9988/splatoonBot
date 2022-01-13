import time
import random
import os
import discord
from PIL import Image
import re
import requests
from bs4 import BeautifulSoup
from utils import IOManager

file_dir = os.path.dirname(os.path.realpath('__file__'))
weapon_icon_path = os.path.join(file_dir, "resources/weapon-icons/")
grizzco_stages_path = os.path.join(file_dir, "resources/grizzco-stages/")
pb_history_path = os.path.join(file_dir, "logs/private-battles-history/")
gj_history_path = os.path.join(file_dir, "logs/grizzco-history/")
token_path = os.path.join(file_dir, "token.txt")

stage_output_width = 300
stage_output_height = 160


# converts struct_time object into in YY-MM-DD-hour-min-sec string
def format_gmtime(gmt):
    result = ('GMT' + str(gmt.tm_year)[2:] + '-' + str(gmt.tm_mon) + '-' +
    str(gmt.tm_mday) + '-' + str(gmt.tm_hour) + 'h-' + str(gmt.tm_min) +
    'm-' + str(gmt.tm_sec) + 's')
    return result

# RETURN a combined image of random weapons
def generate_private_battle(count):
    # get file names
    random_weapon_list = random.sample(os.listdir(weapon_icon_path), k=count)

    img = combine_battle_imgs(random_weapon_list) #TODO combine map and add labels
    return discord.File(img);

def combine_battle_imgs(filename_list):
    max_width = 0
    max_height = 0
    images = []
    for filename in filename_list:
        i = Image.open(os.path.join(weapon_icon_path, filename))
        images.append(i)
        width, height = i.size
        max_width = max(width, max_width)
        max_height = max(height, max_height)

    # align images in 4x2
    total_width = max_width * 2
    total_height = max_height * 4

    new_img = Image.new('RGB', (total_width, total_height))

    img_count = 0
    for y in range(0, 4):
        for x in range(0, 2):
            new_img.paste(images[img_count], (x*max_width,y*max_height))
            x += 1
            img_count += 1
        y += 1

    filepath = io_manager.save_img_to_history(pb_history_path, new_img)
    return filepath


def generate_job_setting():
    random_weapon_list = random.sample(os.listdir(weapon_icon_path), k=4)
    random_grizzco_stage = random.sample(os.listdir(grizzco_stages_path), k=1)
    img = combine_job_imgs(random_weapon_list, random_grizzco_stage[0]) #TODO combine map and add labels
    return discord.File(img);

def combine_job_imgs(weapon_list, stage):
    weapon_side_length = int(stage_output_width/2)
    images = []
    # open imgs
    stage_img = Image.open(os.path.join(grizzco_stages_path, stage))
    stage_img = stage_img.resize((stage_output_width,stage_output_height),Image.ANTIALIAS)
    for f in weapon_list:
        i = Image.open(os.path.join(weapon_icon_path, f))
        i = i.resize((weapon_side_length, weapon_side_length), Image.ANTIALIAS)
        images.append(i)

    # total width = stage icon width
    total_height = int (stage_output_height + weapon_side_length * 2)

    # generate img
    new_img = Image.new('RGB', (stage_output_width, total_height))
    new_img.paste(stage_img, (0, 0))
    img_count = 0
    for y in range(1, 3):
        for x in range (0, 2):
            new_img.paste(images[img_count], (x*weapon_side_length,y*weapon_side_length))
            x += 1
            img_count += 1
        y += 1

    filepath = io_manager.save_img_to_history(gj_history_path, new_img)
    return filepath


# returns counts of records with given key in specified log file
def count_records(filename, key):
    return 1;
    # todo

def get_token():
    with open(token_path, 'r', encoding='UTF-8') as file:
        return file.readline().rstrip();

def get_resources():
    get_weapon_images();
    print("Finished downloading weapon images from splatoonwiki.");

def get_weapon_images():
    print("Downloading weapon images...");
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
        if not os.path.exists(icon_path):
            with open(icon_path, 'wb') as f:
                if 'http' not in url:
                    url = 'https:{}'.format(url)
                response = requests.get(url)
                f.write(response.content)
