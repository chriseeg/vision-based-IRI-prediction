# Warp the perspective of all images in a directory to top-view

from tqdm import tqdm
import os
import cv2 
import numpy as np 

def unwarp(img, src, dst): 
    h, w = 600,600 #img.shape[:2] 
    # use cv2.getPerspectiveTransform() to get M, the transform matrix, and Minv, the inverse 
    M = cv2.getPerspectiveTransform(src, dst) 
    # use cv2.warpPerspective() to warp the image to a top-down view 
    warped = cv2.warpPerspective(img, M, (w, h), flags=cv2.INTER_LINEAR) 

    return warped


#    2  1
#  4      3
# Source points
src = np.float32([(1070, 491), (870, 491), (1600, 1080), (350, 1080)]) 
# Target points
dst = np.float32([(600, 0), (0, 0), (600, 600), (0, 600)]) 


directory = "" #TODO
target_directory = "" #TODO

try:
    os.mkdir(target_directory)
except:
    pass

def crop_image(path,target):
    if path.endswith(".jpg"):
        img = cv2.imread(path) 
        img_crop = unwarp(img, src, dst)
        _ = cv2.imwrite(target, img_crop, [int(cv2.IMWRITE_JPEG_QUALITY), 50]) 

for image in tqdm(os.listdir(directory)):
    crop_image(os.path.join(directory,image),os.path.join(target_directory,image))