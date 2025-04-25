# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta
import ndbc_reader

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

# Get fullpath of wind_per_wav.csv file
wind_per_wav_folder = "C:\\Users\\s44ba\\Documents\\Projects\\JeanettesPier\\Outputs\\"
wind_per_wav_filename = 'wind_per_wav.csv'
wind_per_wav_fullpath = wind_per_wav_folder + wind_per_wav_filename

# Load wind_per_wav to pandas dataframe
# Load space-delimited file into pandas dataframe and set index to column 1, wav_filename_sans_ext
df_wind_per_wav = pd.read_csv(wind_per_wav_fullpath)
df_wind_per_wav.reset_index().set_index('wav_filename_sans_ext')

# Fudge for now, creating a scenario where there will be a duplicate
#df_wind_per_wav = pd.DataFrame({'wind_speed': [3.1,6.1], 'wind_dir': [180.1,160.1]}, index = ['SCW1984_20210421_132000','SCW1984_20210421_142000'])
print("df_wind_per_wav")
print(df_wind_per_wav)

# Specify desired_year, which determines which NDBC ORIN7 file to load.
# We want to load it once and use it for each wav file in a folder.
desired_year = '2021'

# Call ndbc_reader.load_ndbc_file to convert the space-delimited NDBC file into a 
# pandas dataframe. This program converts wind speed to meters/sec at 10 meters above 
# mean sea-level.
df_wind_speeds = ndbc_reader.load_ndbc_file(desired_year)


# Specify folder containing wav files

# Loop through wav files, extracting wav filename sans extension
# For now, fudge one
wav_filename_sans_ext = "SCW1984_20210421_132000"

# Parse wav filename to get timestamp (datetime)
# For now, fudge one
this_timestamp = datetime(2021, 4, 21, 13, 20)

# While in the loop, call ndbc_reader.get_wind_speed
[wind_speed, wind_dir] =  ndbc_reader.get_wind_speed(df_wind_speeds, this_timestamp)

# While still in the loop, stuff wind_speed, wind_dir into a dataframe for this.
# # Set index to be wav_filename_sans_ext 
df_this_row = pd.DataFrame({'wav_filename_sans_ext': [wav_filename_sans_ext], 'wind_speed': [wind_speed], 'wind_dir': [wind_dir]})
df_this_row.reset_index().set_index('wav_filename_sans_ext')
print("df_this_row")
print(df_this_row)

# While still in the loop, insert or update df_wind_per_wav 
# For now, handle case where df_wind_per_wav exists
try:
   df_out = pd.concat([df_wind_per_wav,df_this_row], verify_integrity=True)
except ValueError:
   # Since concat failed (assuming due to duplicate), update instead
   print("WARN: The insert into df_wind_per_wav failed (likely due to duplicate); therefore, updating instead.\n")
   df_wind_per_wav.update(df_this_row)
   df_out =df_wind_per_wav  
finally:
   pass

# Done with loop
# Print
print("df_out")
print(df_out)

# Save to file, overwriting the wind_per_wav csv file
# DO NOT include the index when writing the csv file, as 
# this will mess up the subsequent read of this file.
df_out.to_csv(wind_per_wav_fullpath, index=False)



