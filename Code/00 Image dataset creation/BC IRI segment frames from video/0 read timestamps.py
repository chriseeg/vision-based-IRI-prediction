import pytesseract,os,json
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
from tqdm import tqdm
from multiprocessing import Process, Manager
import pandas as pd

drive_dir = "" #Todo
timestamp_images_dir = "" # TODO: path to raw .jpg images
number_of_parallel_processes = 5
rides_geojson_path = drive_dir + "/02 Development/Data/99 meta/Befahrung_201908.geojson"
target_filepath = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/image_timestamps_.csv"


def open_json(json_path):
	with open(json_path) as f:
		data = json.load(f)
	return data

def crop_timestamp(pil_image):
	# extract timestamp from image
	img = pil_image
	img_crop = img.crop((296, 3, 366, 17))
	return img_crop

def crop_digits(image_pil):
	# Extract single digits from image
	digits = []
	digits.append(image_pil.crop((297, 3, 315, 17)))
	digits.append(image_pil.crop((316, 3, 331, 17)))
	digits.append(image_pil.crop((333, 3, 349, 17)))
	digits.append(image_pil.crop((350, 3, 365, 17)))
	return digits

def get_timestamp_via_digits(image_pil):
	# calculate timestamp via single digits for higher accuracy
	digits_png = crop_digits(image_pil)
	digits = []
	for d in digits_png:
		d = ImageOps.invert(d)
		d = d.resize((d.size[0] * 16, d.size[1] * 16), Image.ANTIALIAS)
		contrast = ImageEnhance.Contrast(d)
		d = contrast.enhance(3)
		digit = pytesseract.image_to_string(d,config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
		digit = digit.replace("\n","")
		digit = digit.replace("\x0c","")
		digits.append(digit)
	raw_string = "".join(digits)
	try:
		seconds = float(digits[2]+"."+digits[3])
		minutes = int(digits[1])
		hours = int(digits[0])
		timestamp_seconds = 3600*hours + 60*minutes + seconds
		return timestamp_seconds, raw_string
	except:
		print(digits)
		return 0,raw_string
	

def get_timestamp(timestamp_path, sophisticated = True):
	image = Image.open(timestamp_path)
	if sophisticated:
		adjusted = image.resize((image.size[0] * 16, image.size[1] * 16), Image.ANTIALIAS)
		adjusted = adjusted.filter(ImageFilter.MinFilter(9))
		adjusted = adjusted.filter(ImageFilter.MaxFilter(9))
		contrast = ImageEnhance.Contrast(adjusted)
		image = contrast.enhance(3)
	try:
		raw_string = pytesseract.image_to_string(image)
		raw_string = raw_string.replace(",917",".91")
		all_digits = [c for c in raw_string if c.isdigit()]
		
		digits = all_digits[-8:]
		seconds = float(digits[4]+digits[5]+"."+digits[6]+digits[7])
		minutes = int(digits[2]+digits[3])
		hours = int(digits[0]+digits[1])
		timestamp_seconds = 3600*hours + 60*minutes + seconds
		return timestamp_seconds,raw_string
	except:
		return None,raw_string

# Get names of rides with IRI scanning
rides_data = open_json(rides_geojson_path)["features"]
rides = [i["properties"]["_VIDEO"] for i in rides_data]

# Get image names
timestamp_images_paths = os.listdir(timestamp_images_dir)
timestamp_images_paths.sort()
print(len(timestamp_images_paths))
# Sort out images that were not part of IRI scanning
timestamp_images_paths = [im for im in timestamp_images_paths if im[:21] in rides]

print(len(timestamp_images_paths))

# split image_paths n lists
paths_splits = [timestamp_images_paths[i::number_of_parallel_processes] for i in range(number_of_parallel_processes)]

timestamps_list = []

def get_timestamps_thread(L, paths):  # the managed list `L` passed explicitly.
	for i,img in enumerate(paths):
		#print(img)
		timestamp_path = os.path.join(timestamp_images_dir,img)
		image = Image.open(timestamp_path)
		timestamp,raw_string = get_timestamp_via_digits(image)

		L.append([img,raw_string,timestamp])

		if i%100 == 0:
			print(i)
		#print(timestamp)

if __name__ == '__main__':
	with Manager() as manager:
		L = manager.list()  # <-- can be shared between processes.
		processes = []
		for i in range(number_of_parallel_processes):
			p = Process(target=get_timestamps_thread, args=(L,paths_splits[i]))  # Passing the list
			p.start()
			processes.append(p)
		for p in processes:
			p.join()
		timestamps_list = list(L)
	    #print(L)
		timestamps_df = pd.DataFrame(timestamps_list)
		timestamps_df.to_csv(target_filepath,index = False,header = False)
#print (str(timestamps_list))


	
#print(timestamps_list)

