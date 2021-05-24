# Combined Image Datasets

### ka_si_C/
- images combined from multiple frames (C )
- one image represents one IRI segment
- images constructed out of bottom row of all video frames of one segment
- resolution: 600:600

### ka_si_BC_IRI.csv
- list of image names in *ka_si_C*
- IRI values of the related IRI segments 
	- IRI level
	- raw value (not used in classification)

### ka_si_BC_damages.csv
- list of image names in *sinsheim_C*
- IRI values of the related IRI segments 
- damage information features extracted from image
	- number of damages
	- estimated total length of damages
	- number of horizontal damages
	- total length of horizontal damages
	- number of vertical damages
	- total length of vertical damages