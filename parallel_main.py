import subprocess
import concurrent.futures
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

def download_in_paralel(iterate_over, multiply_by, chunk_size, original_filename):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        
        for i in range(iterate_over):
            chunk_start = i * multiply_by
            chunk_end = chunk_start + chunk_size
            print(chunk_start, chunk_end)

            futures.append(executor.submit(
                download_chunk, i, original_filename, chunk_start, chunk_end, video_url
            ))

        concurrent.futures.wait(futures)

def download_chunk(chunk_index, original_filename, chunk_start, chunk_end, video_url):
    start_time_str = seconds_to_time(chunk_start)
    end_time_str = seconds_to_time(chunk_end)
    output_filename = f'chunk_{chunk_index + 1:02d}'

    command = [
        'yt-dlp', 
        '--download-sections',
        f'*{str(start_time_str)}-{str(end_time_str)}', 
        '-o', f"/home/miguel/Desktop/DownloadVideo/Data/{original_filename}/{output_filename}", 
        video_url
    ]

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
        stdout, stderr = process.communicate()
        # print(stdout, stderr) # for test purposes 

        if process.returncode != 0:
            print(f"Chunk download failed: {stderr.decode()}")
        else:
            print(f"Chunk {chunk_index + 1} downloaded successfully")

def download_chunks_parallel(video_url):
    original_filename = subprocess.getoutput('yt-dlp --get-filename -o "%(title)s.%(ext)s" ' + video_url)
    duration_obj = subprocess.run(['yt-dlp', '--get-duration', video_url], stdout=subprocess.PIPE, text=True)
    time_obj = time_to_seconds(duration_obj.stdout.strip())
    duration = int(time_obj)

    chunk_size = 30  # sec
    
    FIVE_MINUTES = 300 # sec

    if duration < FIVE_MINUTES:
        times_to_download = int(np.floor(duration / chunk_size))
        download_in_paralel(times_to_download, chunk_size, chunk_size, original_filename)
    else:
        number_of_clips = 10
        one_part = duration / number_of_clips
        download_in_paralel(number_of_clips, one_part, chunk_size, original_filename)


if __name__ == "__main__":
    # video_url = "https://www.youtube.com/watch?v=MI1TlBfPjQs"
    video_url = "https://www.youtube.com/watch?v=HN-WH7C4K0Q"
    download_chunks_parallel(video_url)