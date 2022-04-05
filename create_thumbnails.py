import os
import subprocess

for filename in os.listdir(".\\Memories\\"):
    if filename.endswith(".mp4"):
        subprocess.run(f'ffmpeg -y -i ".\\Memories\\{filename}" -frames:v 1 -q:v 2 -vf '
                       f'"scale=150:150:force_original_aspect_ratio=increase,crop=150:150" '
                       f'".\\Thumbnails\\{filename[:-4]}.jpg"', stdout=subprocess.DEVNULL, check=True)
    elif filename.endswith(".jpg"):
        subprocess.run(f'ffmpeg -hide_banner -loglevel error -y -i ".\\Memories\\{filename}" -q:v 2 -vf '
                       f'"scale=150:150:force_original_aspect_ratio=increase,crop=150:150" '
                       f'".\\Thumbnails\\{filename[:-4]}.jpg"', stdout=subprocess.DEVNULL, check=True)
