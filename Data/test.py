import datetime, subprocess
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
#   if dt.hour > 0:
#     return dt.strftime("%H:%M:%S")  # Include hours if necessary
#   else:
    return dt.strftime("%M:%S")  # Only minutes and seconds if no hours

a = time_to_seconds("09:49")
b = seconds_to_time(a)
print(a, b)

chunk_size = 30  # 30 sec
number_of_clips = 10
one_part = a / number_of_clips

for i in range(number_of_clips):
    chunk_start = i * one_part
    chunk_end = chunk_start + chunk_size
    print(chunk_start, chunk_end, seconds_to_time(chunk_start), seconds_to_time(chunk_end))

video_url = "https://www.youtube.com/watch?v=eq2jMK2KY1Y&t=3s"

def download_chunk(chunk_start, chunk_end, video_url, chunk_number):
    output_filename = f'chunk_{chunk_number + 1:02d}'

    # Build the yt-dlp command
    command = [
        'yt-dlp', 
        '--download-sections',
        f'*{str(chunk_start)}-{str(chunk_end)}', 
        '-o', f"/home/miguel/Desktop/DownloadVideo/Data/{output_filename}", 
        video_url
    ]

    # Using popen
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout, stderr = process.communicate()
        # print(stdout, stderr)

        if process.returncode != 0:
            print(f"Chunk download failed: {stderr.decode()}")
        else:
            print(f"Chunk {chunk_number + 1} downloaded successfully")

# Example usage (assuming you have a way to determine chunk_start and chunk_end)
download_chunk(0, 30, video_url, 0)  # Download the first chunk
download_chunk(30, 60, video_url, 1) # Download the second chunk
# ...and so on
