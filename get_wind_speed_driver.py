# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import ndbc_reader

# Specify desired_year, which determines which NDBC ORIN7 file to load.
# We want to load it once and use it for each wav file in a folder.
desired_year = '2021'

# Call ndbc_reader.load_ndbc_file
df_wind_speeds = ndbc_reader.load_ndbc_file(desired_year)

# Specify folder containing wav files

# Loop through wav files, parsing wav filename to get a timestamp
# For now, fudge one
this_timestamp = datetime(2021, 4, 21, 13, 20)

# While in the loop, call ndbc_reader.get_wind_speed
[wind_speed, wind_dir] =  ndbc_reader.get_wind_speed(df_wind_speeds, this_timestamp)

# Print
print(wind_speed, wind_dir)


