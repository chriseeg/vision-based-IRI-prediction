# Sinsheim Image Datasets


## Image directories
Collections of images used as input for training and testing. (IRI assignment approach in brackets)
### sinsheim_A_crop/
- from original .jpg collection (A)
- cropped to relevant part of the road
- resolution: 776:582

### sinsheim_A_top/
- from original .jpg collection (A)
- warped to top-down perspective
- resolution: 600:600

### sinsheim_B_full/
- image frames extracted from videos 
- one image represents one IRI segment (B)
- resolution: 1920:1080 

### sinsheim_B_crop/
- same image frames as *sinsheim_B_full*
- cropped relevant part of the road
- resolution: 776:582

### sinsheim_B_top/
- same image frames as *sinsheim_B_full*
- cropped relevant part of the road
- resolution: 600:600

### sinsheim_C/
- images combined from multiple frames (C )
- one image represents one IRI segment
- images constructed out of bottom row of all video frames of one segment
- resolution: 600:600


## Image-IRI relations
Lists containing image names and their corresponding IRI value (and additional features)
### sinsheim_A_IRI.csv
- list of image names in *sinsheim_A_[...]*
- IRI values
	- IRI level
	- raw value (not used in classification)
	- assigned via approach A

### sinsheim_BC_IRI.csv
- list of image names in *sinsheim_B_[...]* or *sinsheim_C*
- IRI values of the related IRI segments 
	- IRI level
	- raw value (not used in classification)

### sinsheim_BC_damages.csv
- list of image names in *sinsheim_B_[...]* or *sinsheim_C*
- IRI values of the related IRI segments 
- damage information features extracted from image
	- number of damages
	- estimated total length of damages
	- number of horizontal damages
	- total length of horizontal damages
	- number of vertical damages
	- total length of vertical damages

### sinsheim_BC_IRI binary.csv
- list of image names in *sinsheim_B_[...]* or *sinsheim_C*
- IRI values of the related IRI segments
	- binary class assignment
	- raw value (not used in classification)


### sinsheim_BC_IRI fine.csv
- list of image names in *sinsheim_B_[...]* or *sinsheim_C*
- IRI values of the related IRI segments
	- class assignment with 10 levels
	- raw value (not used in classification)

### sinsheim_BC_IRI mehrspurig außerorts.csv
- same columns as *sinsheim_BC_IRI.csv*
- only images of street type *mehrspurig außerorts*

### sinsheim_BC_IRI mehrspurig außerorts ohne erneuerte Fahrbahn.csv
- same file as *sinsheim_BC_IRI mehrspurig außerorts.csv* but without images from renewed A6 roadway section
