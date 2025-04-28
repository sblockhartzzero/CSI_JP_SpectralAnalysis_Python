# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import ndbc_reader
import wind_per_wav


'''''
To do:
-Handle case where wind_per_wav.csv does not yet exist.
-Loop on wav files per folder
-Remove fudge

'''''

# If the wind_per_wav.csv file exists, load it into a pandas dataframe.
# As we loop through the wav files in a folder (below), we will be inserting or updating 
# this dataframe, one row at a time. This way, we avoid duplicates. 
# Finally, after looping through all the wav files in the folder, we will overwrite 
# the wind_per_wav.csv file.

'''''
USER INPUT:
'''''
# Specify desired_year, which determines which NDBC ORIN7 file to load.
# We want to load it once and use it for each wav file in a folder.
desired_year = '2021'

# Get fullpath of wind_per_wav.csv file
wind_per_wav_folder = "C:\\Users\\s44ba\\Documents\\Projects\\JeanettesPier\\Outputs\\"
wind_per_wav_filename = 'wind_per_wav.csv'

# Specify folder containing wav files


'''''
LOAD FILES to PANDAS DATAFRAMES:
'''''
# Load the space-delimited NDBC ORIN7 file into a pandas dataframe df_wind_speeds. 
# This program converts wind speed to meters/sec at 10 meters above mean sea-level.
df_wind_speeds = ndbc_reader.load_ndbc_file(desired_year)

# Load existing wind_per_wav.csv (if it exists) to the pandas dataframe df_wind_per_wav
wind_per_wav_fullpath = wind_per_wav_folder + wind_per_wav_filename
df_wind_per_wav = wind_per_wav.load_wind_per_wav(wind_per_wav_fullpath)
print("df_wind_per_wav")
print(df_wind_per_wav)
print("\n")


'''''
ADD ROWS to df_wind_per_wav (INSERT OR UPDATE):
'''''
# Loop through wav files, extracting wav filename sans extension
# For now, fudge one
wav_filename_sans_ext = "SCW1984_20210421_132000"

# Parse wav filename to get timestamp (datetime)
# For now, fudge one
this_timestamp = datetime(2021, 4, 21, 13, 20)

# While in the loop, call ndbc_reader.get_wind_speed to get wind_speed and wind_dir
# for this wav file
[wind_speed, wind_dir] =  ndbc_reader.get_wind_speed(df_wind_speeds, this_timestamp)
print(wind_speed, wind_dir)
print("\n")

# Using wav_filename_sans_ext, wind_speed, wind_dir for this wav file, add this
# information to the pandas dataframe df_wind_per_wav
df_out = wind_per_wav.insert_or_update(df_wind_per_wav, wav_filename_sans_ext, wind_speed, wind_dir)

# Done with loop
# Print
print("df_out")
print(df_out)
print("\n")


'''''
SAVE df_wind_per_wav to NEW wind_per_wav.csv:
'''''
# Save to file, overwriting the existing wind_per_wav csv file (if one exists)
wind_per_wav.save(df_wind_per_wav, wind_per_wav_fullpath)




