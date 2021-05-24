# Create datasets B & C

## 0 read timestamps.py
- Extract date and time from timestamp in .jpg images. These are used to synchronize video frames and IRI segments.

## 1 get video times for frames.py
- Extract date and time from timestamp in video frames.

## 2 get frame from segment.py
- Identify a video frame for every IRI segemnt via the extracted timestamps.

## 2b get frame rows from segment.py
- For approach C: Extract all video frames of a segment. Then warp and crop them to create high-res top-down image.

## 3 create IRI segment dataset.py
- Create .csv file containing image name and corresponding IRI value.

## frame_timestamps_karlsruhe.csv
- Extracted and corrected timestamp values of video frames in KA dataset.

## frame_timestamps_sinsheim.csv
- Extracted and corrected timestamp values of video frames in SI dataset.

## image_timestamps_karlsruhe.csv
- Extracted and corrected timestamp values of .jpg images in KA dataset.

## image_timestamps_sinsheim.csv
- Extracted and corrected timestamp values of .jpg images in SI dataset.