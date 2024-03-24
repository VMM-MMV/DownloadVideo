import datetime
import numpy as np

def time_to_seconds(time_str):
    """Converts a time string (HH:MM) to total seconds."""
    time_strs = time_str.split(":")
    if len(time_strs) == 3:
        return int(time_strs[0])*3600 + int(time_strs[1]) * 60 + int(time_strs[2])
    if len(time_strs) == 2:
        return (int(time_strs[0])*60) + int(time_strs[1])

def seconds_to_time(seconds):
    """Converts seconds to a formatted time string with hours, minutes, and seconds."""
    
    dt = datetime.datetime.fromtimestamp(seconds)
    if seconds > 3600:
        time_str = dt.strftime(f"%H:%M:%S")
        first_cut = time_str.find(":")
        return str(int(time_str[:first_cut])-3) + time_str[first_cut:] # Include hours if necessary
    else:
        return dt.strftime("%M:%S")  # Only minutes and seconds if no hours
    
def handle_less_than_5():
    a = time_to_seconds("4:49")
    chunk_size = 30
    times_to_download = int(np.floor(a / chunk_size))
    print(times_to_download)
    for i in range(times_to_download):
        print(seconds_to_time(30*i))

    
handle_less_than_5()