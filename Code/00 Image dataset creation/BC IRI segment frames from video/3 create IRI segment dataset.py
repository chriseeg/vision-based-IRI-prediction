import json, os
import pandas as pd
from tqdm import tqdm

# create csv with IRI values of segments
drive_dir = "" #TODO: define location of drive
iri_geojson_path =   drive_dir + "/02 Development/Data/99 meta/IRI_201908.geojson"
segment_images_dir = drive_dir + "/02 Development/Code/00 Image dataset creation/BC IRI segment frames from video/sinsheim_segment_imagestrips_adaptive"

target_filepath = drive_dir + "/02 Development/Data/01 IRI prediction/01 Sinsheim/sinsheim_BC_IRI.csv"

def open_json(json_path):
	with open(json_path) as f:
		data = json.load(f)
	return data

iri_data = open_json(iri_geojson_path)["features"]
segment_images = os.listdir(segment_images_dir)

result_data = []
for segment in tqdm(iri_data):
	ride = segment["properties"]["VIDEO"]
	sgm_nr = ("0000" + segment["properties"]["Abnr"])[-5:]
	segment_id = ride + "_sgm" + sgm_nr + ".jpg"
	
	if segment_id in segment_images:
		iri_class = segment["properties"]["IRIC_CLASS"]
		iri_value = segment["properties"]["IRIC_m_km"]

		if iri_class == "NV":
			continue
		result_data.append([segment_id,iri_class,iri_value])
print(len(segment_images))
print(len(result_data))
result_df = pd.DataFrame(result_data)
result_df.to_csv(target_filepath,index = False,header = False)


