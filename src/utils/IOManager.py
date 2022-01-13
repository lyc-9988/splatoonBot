import os
import utils
from PIL import Image
import psycopg2

# DATABASE_URL = os.environ['DATABASE_URL']
# conn = psycopg2.connect(DATABASE_URL, sslmode='require')

# save img to parent_path with current time in filename
# RETURN filepath of saved image
def save_img_to_history(parent_path, img):
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    filepath = os.path.join(parent_path, utils.format_gmtime(time.gmtime())) + ".png"
    img.save(filepath)
    return filepath
