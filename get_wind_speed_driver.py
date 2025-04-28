# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import os
import ndbc_reader
import wind_per_wav
import wav_Helper


'''''
To do:
-Handle case where wind_per_wav.csv does not yet exist.
-Why is it updating instead of inserting (for 2nd row of test data)? Issue with index, so just code it to avoid dup on wav_filename_sans_ext

'''''

# If the wind_per_wav.csv file exists, load it into a pandas dataframe df_wind_per_wav.
# Below, as we loop through the wav files in a folder, we will be adding to 
# this dataframe, one row at a time. If the insert would produce a duplicate,
# perform an update. Finally, after looping through all the wav files in the folder, 
# we will overwrite the wind_per_wav.csv file.

'''''
USER INPUT:
'''''
# Specify desired_year, which determines which NDBC ORIN7 file to load.
# We want to load it once and use it for each wav file in a folder.
desired_year = '2021'

# Get fullpath of wind_per_wav.csv file
wind_per_wav_fullpath = "C:\\Users\\s44ba\\Documents\\Projects\\JeanettesPier\\Outputs\\wind_per_wav.csv"

# Specify folder containing wav files
# This program will loop through all the wav files in this folder
wav_folder = "C:\\Users\\s44ba\\Documents\\Projects\\JeanettesPier\\Data\\Test\\"


'''''
LOAD FILES to PANDAS DATAFRAMES:
'''''
# Load the space-delimited NDBC ORIN7 file into a pandas dataframe df_wind_speeds. 
# This program converts wind speed to meters/sec at 10 meters above mean sea-level.
df_wind_speeds = ndbc_reader.load_ndbc_file(desired_year)

# Load existing wind_per_wav.csv (if it exists) to the pandas dataframe df_wind_per_wav
df_wind_per_wav = wind_per_wav.load_wind_per_wav(wind_per_wav_fullpath)

# Print out before the update
print("INFO: df_wind_per_wav BEFORE insert/update:")
print(df_wind_per_wav)
print("\n")


'''''
ADD ROWS to df_wind_per_wav (INSERT OR UPDATE):
'''''
# Get list of wav filenames in the wav_folder
dir_list = os.listdir(wav_folder)

# Loop through files, extracting wav filename sans extension
for filename in dir_list:
    if ".wav" in filename:
        # This is a wav file, so process
        # Extract wav filename without extension
        wav_filename_sans_ext = filename[:-4]

        # Derive timestamp from wav filename
        this_timestamp = wav_Helper.xlat_filename_to_datetime(wav_filename_sans_ext)

        # While in the loop, call ndbc_reader.get_wind_speed to get wind_speed and wind_dir
        # for this wav file
        [wind_speed, wind_dir] =  ndbc_reader.get_wind_speed(df_wind_speeds, this_timestamp)
        print("INFO: Getting ready to add new row to df_wind_per_wav:")
        print(wav_filename_sans_ext, wind_speed, wind_dir)
        print("\n")

        # Using wav_filename_sans_ext, wind_speed, wind_dir for this wav file, add this
        # information to the pandas dataframe df_wind_per_wav
        df_out = wind_per_wav.insert_or_update(df_wind_per_wav, wav_filename_sans_ext, wind_speed, wind_dir)

        # Set df_wind_per_wav to this updated df (so the next iteration of the loop gets the updated df)
        df_wind_per_wav = df_out

        # Print
        print("INFO: df_wind_per_wav AFTER insert/update:")
        print(df_wind_per_wav)
        print("\n")

    # endif
# end loop


'''''
SAVE df_wind_per_wav to NEW wind_per_wav.csv:
'''''
# Save to file, overwriting the existing wind_per_wav csv file (if one exists)
wind_per_wav.save(df_wind_per_wav, wind_per_wav_fullpath)




