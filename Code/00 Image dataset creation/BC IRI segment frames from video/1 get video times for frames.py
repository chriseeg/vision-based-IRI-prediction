import cv2, os, json, csv
import geopy.distance as geo
import numpy as np
import pandas as pd
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract

# get timestamp for every 10 frames in a video

drive_dir = "" #TODO: define location of drive
rides_geojson_path = drive_dir + "/02 Development/Data/99 meta/Befahrung_201908.geojson"
image_timestamps_path = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/image_timestamps_sinsheim.csv"
videos_dir = ".../VIDEOS/Videos" #TODO: change to original video directory
target_dir = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/segment_frames"
failed_frames_save_dir = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/failed frames"
target_csv_path = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/"


def get_frames_timestamps(video_path):
	result_list = []
	cap= cv2.VideoCapture(video_path)
	frame_count=0
	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == False:
			break
		if frame_count % 10 == 0:
			frame_pil = Image.fromarray(frame)
			#frame_pil.show()
			timestamp = get_timestamp_via_digits(frame_pil)
			if timestamp == None:
				print("ups")
				print(raw_string)
				timestamp = 0
				frame_crop = crop_timestamp(frame_pil)
				frame_crop.save(os.path.join(failed_frames_save_dir,frame_count+".png"))

			# Calculate values for round two
			result_list.append([frame_count, timestamp])

		if frame_count % 1000 == 0:
			print("{} frames done".format(frame_count))
		frame_count+=1

	cap.release()
	cv2.destroyAllWindows()

	return result_list

def open_json(json_path):
	with open(json_path) as f:
		data = json.load(f)
	return data

def open_csv(path):
	with open(path, mode='r') as infile:
		reader = csv.reader(infile)
		data_list = [rows for rows in reader]
	return data_list

def crop_timestamp(pil_image):
	img = pil_image
	img_crop = img.crop((296, 3, 366, 17))
	return img_crop

def crop_digits(frame_pil):
  digits = []
  digits.append(frame_pil.crop((297, 3, 315, 17)))
  digits.append(frame_pil.crop((316, 3, 331, 17)))
  digits.append(frame_pil.crop((333, 3, 349, 17)))
  digits.append(frame_pil.crop((350, 3, 365, 17)))
  return digits

def get_timestamp_via_digits(frame_pil):
	digits_png = crop_digits(frame_pil)
	digits = []
	for d in digits_png:
		d = ImageOps.invert(d)
		d = d.resize((d.size[0] * 16, d.size[1] * 16), Image.ANTIALIAS)
		contrast = ImageEnhance.Contrast(d)
		d = contrast.enhance(3)
		#d.show()
		digit = pytesseract.image_to_string(d,config='--psm 13 --oem 3 -c tessedit_char_whitelist=0123456789')
		digit = digit.replace("\n","")
		digit = digit.replace("\x0c","")
		digits.append(digit)
	seconds = float(digits[2]+"."+digits[3])
	minutes = int(digits[1])
	hours = int(digits[0])
	timestamp_seconds = 3600*hours + 60*minutes + seconds
	raw_string = "".join(digits)
	#print(raw_string)
	return timestamp_seconds


rides_data = open_json(rides_geojson_path)["features"]
rides = [i["properties"]["_VIDEO"] for i in rides_data]
 
results = []
# iterate rides
for ride in rides[2:3]:

	video_path = os.path.join(videos_dir, ride + ".asf")

	# Round one
	print("Start scanning ride {}".format(ride))
	result_list = get_frames_timestamps(video_path)



	result_df = pd.DataFrame(result_list)
	result_df['ride'] = ride
	results.append(result_df)

results_df = pd.concat(results)
results_df.to_csv(target_csv_path,index = False,header = False)
