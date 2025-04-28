# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta

'''''

'''''

def load_wind_per_wav(wind_per_wav_fullpath):

    # Load wind_per_wav to pandas dataframe
    # Load space-delimited file into pandas dataframe and set index to column 1, wav_filename_sans_ext
    df = pd.read_csv(wind_per_wav_fullpath)
    df_wind_per_wav = df.set_index('wav_filename_sans_ext')

    # Return
    return df_wind_per_wav


def insert_or_update(df_wind_per_wav, wav_filename_sans_ext, wind_speed, wind_dir):
    
    # Stuff wav_filename_sans_ext, wind_speed, wind_dir into a dataframe df_this_row
    # This is a single row, formatted like df_wind_per_wav
    df = pd.DataFrame({'wav_filename_sans_ext': [wav_filename_sans_ext], 'wind_speed': [wind_speed], 'wind_dir': [wind_dir]})
    df_this_row = df.set_index('wav_filename_sans_ext')

    # Print
    print("INFO: df_this_row:")
    print(df_this_row)
    print("\n")

    # Update df_wind_per_wav with the single row df_this_row.
    # If the insert (i.e. concat with integrity) fails, do an update 
    try:
       df_out = pd.concat([df_wind_per_wav,df_this_row], verify_integrity=True)
    except ValueError:
       # Since concat failed (assuming due to duplicate), update instead
       print("WARN: The insert into df_wind_per_wav failed (likely due to duplicate); therefore, updating instead.\n")
       df_wind_per_wav.update(df_this_row)
       df_out =df_wind_per_wav  
    finally:
       pass
    
    # Return
    return df_out


def save(df_wind_per_wav, wind_per_wav_fullpath):

    # Save to file, overwriting the wind_per_wav csv file
    df_wind_per_wav.to_csv(wind_per_wav_fullpath, index=True)

