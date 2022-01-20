import sys, os
import subprocess
from pprint import pprint


os.system("title " + "Merge Laracast Video & Audio")

if len(sys.argv) != 3:
    input("Drop two files (a video and an audio file) on this python script.")
    sys.exit()

dir_path      = os.path.dirname(sys.argv[1])
file_name_ext = os.path.basename(sys.argv[1])
file_name     = os.path.splitext(file_name_ext)[0].split("_")[0]

video_path  = sys.argv[1]
audio_path  = sys.argv[2]

output_path = dir_path + "\\" + file_name + ".mp4"

subprocess.call([
    "C:/Program Files/ffmpeg/bin/ffmpeg.exe",
    "-i",
    video_path,
    "-i",
    audio_path,
    "-vcodec",
    "copy",
    "-acodec",
    "copy",
    output_path,
])

input("\nDONE!")
