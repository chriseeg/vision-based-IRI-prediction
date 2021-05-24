# Crop all images in a directory to the coordinates

from PIL import Image
from tqdm import tqdm
import os

coordinates = (572, 420, 1348, 1080)
directory = "" #TODO
target_directory = "" #TODO


def crop_image(path,target):
    if path.endswith(".jpg"):
        img = Image.open(path)
        img_crop = img.crop(coordinates)
        img_crop.save(target, "JPEG", quality=40, optimize=True)

for image in tqdm(os.listdir(directory)):
    crop_image(os.path.join(directory,image),os.path.join(target_directory,image))