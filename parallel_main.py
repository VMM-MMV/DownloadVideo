import subprocess
import concurrent.futures
import datetime

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
    if dt.hour > 0:
        return dt.strftime("%H:%M:%S")  # Include hours if necessary
    else:
        return dt.strftime("%M:%S")  # Only minutes and seconds if no hours

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

    FIVE_MINUTES = 300 # sec
    if duration < FIVE_MINUTES:
        print("Video is shorter than 5 minutes. Skipping...")
        return

    chunk_size = 30  # sec
    number_of_clips = 10
    one_part = duration / number_of_clips
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for i in range(number_of_clips):
            chunk_start = i * one_part
            chunk_end = chunk_start + chunk_size
            futures.append(executor.submit(
                download_chunk, i, original_filename, chunk_start, chunk_end, video_url
            ))

        concurrent.futures.wait(futures)

if __name__ == "__main__":
    video_url = "https://www.youtube.com/watch?v=HN-WH7C4K0Q"
    download_chunks_parallel(video_url)
