
Data
1. Video_details

Information about which first (and last) frame of data should be used in order for each video to be correctly synchronized (in some cases the total video length was half a second longer than a whole number, the start of each video is not sychronized since record was pressed at different times, 3 seconds apart, on each camera).

2. Colony_1/Colony_1_low_density_camera_4/GP014620_454.txt (for example)

These are the raw data files created from running the tracking software, Clicky.py

3. measurements.csv

A spreadsheet containing the coordinates of reference points in the raw tracking data (necessary for transforming location coordinates pixel values to values in mm)


Code
1. Compile_text_files.py

Reads the raw data files for a given colony number (1,2 or 3) and density treatment (high or low) and the video details file. These values are hard-coded and can be changed by editing lines 7 and 8 of the script. The output is a file for every ant in the specified colony number and density treatment. Output is in the form 

Colony_1_low_density_locations/454_locations.txt (for example)

2. one_nest_edit.py

To be run after raw data files have been compiled using "Compile_text_files.py". Also uses "measurements.csv". Output is the transformed data in mm values with the entrance at 0,0. Output is in the form

Corrected/Colony_1_low_density_corrected/454_locations.txt (for example)

3. interpolate.py

To be run after raw data files have been corrected using "one_nest_edit.py". Output is the same data but with interpolated values added for the times when an ant is between boxes and therefore not recorded by any camera. Output is in the form

Interpolated/Colony_1_low_density_interpolated/454_locations.txt (for example)

4. put_ants_back_in_the_box.py

To be run after raw data files have been interpolated using "interpolate.py". Output is the same data but with adjustments made to those locations that appear to be outside of the nest region. Output is in the form

Boxed/Colony_1_low_density_boxed/454_locations.txt (for example)

This is the final data. 






