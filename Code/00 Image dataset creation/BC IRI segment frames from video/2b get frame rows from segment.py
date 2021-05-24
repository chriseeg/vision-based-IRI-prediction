import cv2, os, json, csv
import geopy.distance as geo
import numpy as np
import pandas as pd
from tqdm import tqdm
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import pytesseract

# Identify all video-frames for every IRI-Segment and put them together


# Open IRI-segments, image-capture and ride-list file
drive_dir = "" #TODO: define location of drive
iri_geojson_path =   drive_dir + "/02 Development/Data/99 meta/IRI_201908.geojson"
image_geojson_path = drive_dir + "/02 Development/Data/99 meta/Aufnahmepunkte_GeoJPG_201908.geojson"
rides_geojson_path = drive_dir + "/02 Development/Data/99 meta/Befahrung_201908.geojson"
image_timestamps_path = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/image_timestamps_sinsheim.csv"
frame_timestamps_path = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/frame_timestamps_sinsheim.csv"
videos_dir = ".../VIDEOS/Videos" #TODO: change to original video directory
temp_dir = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/Segment Frames Rows adaptive"
target_dir = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/sinsheim_segment_imagestrips_adaptive"

try:
    os.mkdir(temp_dir)
except:
    pass

try:
    os.mkdir(target_dir)
    print("yeah")
except:
    pass

def open_json(json_path):
	with open(json_path) as f:
		data = json.load(f)
	return data

def open_csv(path):
	with open(path, mode='r') as infile:
		reader = csv.reader(infile)
		data_list = [rows for rows in reader]
	return data_list

def get_2_closest_images(segm_coordinates, ride_video, img_data, reference_image_name):  
  p1 = (segm_coordinates[1],segm_coordinates[0])
  distances_imgs = []
  ride_imgs = []

  for img in img_data:
    if img["properties"]["NAME"][:21] == ride_video:
      image_name = img["properties"]["NAME"]
      ride_imgs.append(img)
      p2 = (img["geometry"]["coordinates"][1],img["geometry"]["coordinates"][0])    
      distance = geo.distance(p1,p2).km
      distances_imgs.append([distance,image_name])

    # if img["properties"]["DATE"]+"_"+img["properties"]["TIME"] == ride_video:
    #   image_name = img["properties"]["NAME"]
    #   ride_imgs.append(img)
    #   p2 = (img["geometry"]["coordinates"][1],img["geometry"]["coordinates"][0])    
    #   distance = geo.distance(p1,p2).km
    #   distances_imgs.append([distance,image_name])

  # closest two distances
  distances_imgs.sort()
  result_distances = [distances_imgs[0][0], distances_imgs[1][0]]
  result_names = [distances_imgs[0][1], distances_imgs[1][1]]
  # check if images are close to each other
  image_numbers = [int(i.split("_")[2].split(".")[0]) for i in result_names]
  if abs(image_numbers[1]-image_numbers[0]) > 5:
  	print("ups")
  	reference_image_number = 1 + int(reference_image_name.split("_")[2].split(".")[0])
  	close_names = [i[1] for i in distances_imgs[:4]]
  	if abs(image_numbers[0] - reference_image_number) > 5:
  		# First number is wrong
  		# Get image with closest number to reference number among 7 closest images
  		min_number_distance = 9999
  		for i in distances_imgs[:8]:
  			n = int(i[1].split("_")[2].split(".")[0])
  			if not n in image_numbers:
	  			number_distance = abs(n - reference_image_number)
	  			if min_number_distance > number_distance:
	  				min_number_distance = abs(n - reference_image_number)
	  				result_distances[0] = i[0]
	  				result_names[0] = i[1]

  	elif abs(image_numbers[1] - reference_image_number) > 5:
  		# Second number is wrong
  		# Get image with closest number to reference number among 4 closest images
  		min_number_distance = 9999
  		for i in distances_imgs[:5]:
  			n = int(i[1].split("_")[2].split(".")[0])
  			if not n in image_numbers:
	  			number_distance = abs(n - reference_image_number)
	  			if min_number_distance > number_distance:
	  				min_number_distance = abs(n - reference_image_number)
	  				result_distances[1] = i[0]
	  				result_names[1] = i[1]
  weighted_distances = [d/sum(result_distances) for d in result_distances]
  result = {
  	result_names[0] : weighted_distances[0],
  	result_names[1] : weighted_distances[1]
  }
  result_image_names = sorted(result)
  result_weighted_distances = [result[result_image_names[0]],result[result_image_names[1]]]
  return result_image_names, result_weighted_distances

def get_2_closest_frames(timestamp,ride_video,frame_timestamps_data):
	frame_min_d = 0
	frame_min_d2 = 0
	min_d = 99999999
	min_d2 = 99999999
	for r,f,t in frame_timestamps_data:
		if r == ride_video:
			d = abs(timestamp - t)
			if d < min_d:
				frame_min_d2 = frame_min_d
				frame_min_d = f
				min_d2 = min_d
				min_d = d
			elif d < min_d2:
				frame_min_d2 = f
				min_d2 = d

	min_d = min_d/(min_d+min_d2)
	min_d2 = min_d2/(min_d+min_d2)

	if frame_min_d > frame_min_d2:
		return [[frame_min_d2,frame_min_d],[min_d2,min_d]]
	else:
		return [[frame_min_d,frame_min_d2],[min_d,min_d2]]

def crop_warp_image(img,warp_src,warp_dst,size,row_height):
	img_warped = unwarp(img, warp_src, warp_dst, size)
	inv_row_height = size - row_height
	img_crop = img_warped[inv_row_height - 15:size-15, 0:size]
	return img_crop

def unwarp(img, src, dst, size): 
	h, w = size,size #img.shape[:2] 
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse 
	M = cv2.getPerspectiveTransform(src, dst) 
    # use cv2.warpPerspective() to warp the image to a top-down view 
	warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR)
	return warped

def save_frames(video_path,frames_dict,target_dir, warp_src, warp_dst, size):
	
	cap= cv2.VideoCapture(video_path)
	i=0

	segm_count = 0
	max_count = len(frames_dict)
	pbar = tqdm(total=max_count)

	while(cap.isOpened()):
		ret, frame = cap.read()
		if ret == False:
			break
		if segm_count >= max_count:
			break
		if i in frames_dict:
			nr_rows = frames_dict[i]["nr_rows"]
			# Adapt height of last image strip
			if int(frames_dict[i]["id"].split("row")[1]) != nr_rows-1:
				row_height = round(size/nr_rows)
			else:
				row_height = size - (nr_rows-1) * round(size/nr_rows)
			if row_height > 0:
				frame = crop_warp_image(frame, warp_src, warp_dst, size, row_height)
				try:
					cv2.imwrite(os.path.join(target_dir,frames_dict[i]["id"]+'.jpg'),frame)
				except:
					print("Fail! " + frames_dict[i]["id"], i, row_height, nr_rows)
			segm_count += 1
			pbar.update(1)
		i+=1

	pbar.close()
	cap.release()
	cv2.destroyAllWindows()

def get_segm_nr(filename):
    nr = int(filename.split("sgm")[1].split("_")[0])
    return nr

def get_row_nr(filename):
    nr = int(filename.split("row")[1].split(".")[0])
    return nr

def join_images(images):
    cropped_images = []

    for image in images:
        img_path = os.path.join(temp_dir,image)
        image = cv2.imread(img_path)
        cropped_images.append(image)
    cropped_images.reverse()
    joined_image = np.concatenate(cropped_images, axis = 0)
    return joined_image




iri_data = open_json(iri_geojson_path)["features"]
img_data = open_json(image_geojson_path)["features"]

img_timestamps_data = open_csv(image_timestamps_path)
img_timestamps_dict = {i[0]: float(i[1]) for i in img_timestamps_data}

frame_timestamps_data = open_csv(frame_timestamps_path)
frame_timestamps_data = [[i[0],int(i[1]),float(i[2])]  for i in frame_timestamps_data] #ride_name,frame,timestamp

rides_data = open_json(rides_geojson_path)["features"]
rides = [i["properties"]["_VIDEO"] for i in rides_data]
rides.sort()
# iterate rides
print(rides)
if True:
	for i_r,ride in enumerate(rides[4:5]):
		print("ride: {} of {} ({})".format(i_r,len(rides),ride))
		
		segment_frames_dict = {}
		
		hours = int(ride[9:11])
		minutes = int(ride[12:14])
		seconds = float(ride[15:].replace("-","."))
		# time of first image of ride (seconds)
		t_start = 3600*hours + 60*minutes + seconds
		#print(hours,minutes,seconds)
		print("t_start: " + str(t_start))

		ride_iri_data = [i for i in iri_data if i["properties"]["VIDEO"] == ride]
		pbar = tqdm(total=len(ride_iri_data))
		reference_image_name = "20190814_10-24-58-435_0001.jpg"

		# Read start point coordinates & IRI values of each segment
		for segment in iri_data:
			pbar.update(1)
			if segment["properties"]["VIDEO"] == ride:
				sgm_nr = "0000" + segment["properties"]["Abnr"]

				segment_id = ride + "_sgm" + sgm_nr[-5:]
				start_position = segment["geometry"]["coordinates"][0]

				# Calculate approximate time of each segment start position
				#   1. look for the two images closest to the segment-start and get the corresponding distances
				closest_image_names, weighted_distances = get_2_closest_images(start_position,ride,img_data,reference_image_name)
				reference_image_name = closest_image_names[1]
				d0, d1 = weighted_distances
				
				#   2. Get time from images
				t0 = img_timestamps_dict[closest_image_names[0]]
				t1 = img_timestamps_dict[closest_image_names[1]]
				
				#   3. interpolate time of segment beginning
				t_s0 = t0 + d0 / (d0 + d1) * (t1 - t0) + 0.3 # adding 0.3 seconds of deviation 
				
				#   4. get closest frames in frame_time_converter based on t_s0
				closest_frames, weighted_distances = get_2_closest_frames(t_s0, ride,frame_timestamps_data)
				f0,f1 = closest_frames
				d0,d1 = weighted_distances
				
				#   5. interpolate frame number corresponding to segment beginning
				f_s0 = round(f0 + d0 / (d0 + d1) * (f1 - f0))
				#print(f_s0)
				#print(segment_id)
				#print(closest_image_names)
				#print("time s0: " + str(t_s0))
				#print(closest_frames)
				#print(weighted_distances)
				#print("frame s0: " + str(f_s0))

				segment_frames_dict[f_s0] = segment_id

		pbar.close()

		# Calculate frame numbers for n rows that will be connected
		row_frames_dict = {}
		size = 600
		# Source- and destination points for warping
		warp_src = np.float32([(1070, 491), (870, 491), (1600, 1080), (350, 1080)]) 
		warp_dst = np.float32([(size, 0), (0, 0), (size, size), (0, size)]) 

		start_frame_nrs = list(segment_frames_dict.keys())
		for i,start_frame in enumerate(start_frame_nrs):
			if i == len(start_frame_nrs) - 1:
				break
			segment_id = segment_frames_dict[start_frame]
			end_frame = start_frame_nrs[i+1]
			frames_per_row = end_frame - start_frame

			for r in range(frames_per_row):
				segment_row_id = segment_id + "_row" + ("000" + str(r))[-3:]
				frame_nr = start_frame + r
				row_frames_dict[frame_nr] = {"id": segment_row_id, "nr_rows": frames_per_row}

		video_path = os.path.join(videos_dir, ride + ".asf")
		print("Start frame extraction for ride {}".format(ride))
		
		save_frames(video_path,row_frames_dict,temp_dir, warp_src, warp_dst, size)

# Join image strips
print("Start joining image strips.")

images_list = os.listdir(temp_dir)

for ride in rides[4:5]:
	ride_images_list = [i for i in images_list if i[:21] == ride]
	ride_images_list.sort()
	nr_segments = get_segm_nr(ride_images_list[-1]) + 1 
	segments = [[] for i in range(nr_segments)]

	for image in ride_images_list:
		segm_nr = get_segm_nr(image)
		segments[segm_nr].append(image)

	for segm_images in tqdm(segments):
		if segm_images:
			target_image_name = "_".join(segm_images[0].split("_")[0:3])+".jpg"
			target = os.path.join(target_dir,target_image_name)
			joined_image = join_images(segm_images)
			_ = cv2.imwrite(target, joined_image, [int(cv2.IMWRITE_JPEG_QUALITY), 70])

