import subprocess

command = [
    'yt-dlp',
    '--download-sections',
    '*1:30-1:45',
    'https://www.youtube.com/watch?v=HN-WH7C4K0Q'
]


completed_process = subprocess.run(command, check=True) 