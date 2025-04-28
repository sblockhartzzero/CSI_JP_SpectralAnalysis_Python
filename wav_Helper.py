# Imports
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
from datetime import timedelta

'''''

'''''

def xlat_filename_to_datetime(wav_filename_sans_ext):
    
    # wav filename formatted like: SCW1984_20210421_132000

    # Parse wav filename to get timestamp (datetime)
    # What is index of first underscore?
    pos_us1 = wav_filename_sans_ext.find("_")
    # Extract YYYYMMDD_hhmmss string
    start_pos = pos_us1 + 1
    this_formatted_datetime = wav_filename_sans_ext[start_pos:]
    # Convert to datetime
    this_datetime_format = "%Y%m%d_%H%M%S"
    this_timestamp = datetime.strptime(this_formatted_datetime, this_datetime_format)

    # Return
    return this_timestamp

