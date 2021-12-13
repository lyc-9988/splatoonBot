import time
import random
import os
import discord
from PIL import Image

weaponDir = "resources/weaponIcons/"
privateBattlesDir = "logs/privateBattles/"
tokenFile = "token.txt"


# converts struct_time object into in YY-MM-DD-hour-min-sec string
def format_gmtime(gmt):
    result = ('GMT' + str(gmt.tm_year)[2:] + '-' + str(gmt.tm_mon) + '-' +
    str(gmt.tm_mday) + '-' + str(gmt.tm_hour) + 'h-' + str(gmt.tm_min) +
    'm-' + str(gmt.tm_sec) + 's')
    return result

# returns a combined image of random weapons
def generate_private_battle(count):
    # get file names
    random_weapon_list = random.sample(os.listdir(weaponDir), k=count)

    img = combine_imgs(random_weapon_list)
    return discord.File(img);
    # filename = os.path.join(weaponDir, random_weapon_list[0])
    # with open(filename, 'rb') as f:
    #   return discord.File(f);

def combine_imgs(filename_list):
    max_width = 0
    max_height = 0
    images = []
    for filename in filename_list:
        i = Image.open(os.path.join(weaponDir, filename))
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
        y -= 1

    filepath = os.path.join(privateBattlesDir, format_gmtime(time.gmtime())) + ".png"
    # filepath = 'test.png'
    if not os.path.exists(privateBattlesDir):
        os.makedirs(privateBattlesDir)
    new_img.save(filepath)
    return filepath


# returns counts of records with given key in specified log file
def count_records(filename, key):
    return 1;
    # todo

def get_token():
    with open(tokenFile, 'r', encoding='UTF-8') as file:
        return file.readline().rstrip();
