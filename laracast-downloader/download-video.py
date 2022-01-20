import sys
import traceback
import requests
import json
from pprint import pprint
import os
import base64


os.system("title " + "Download Laracast Video")

EXIT_MSG = "\nProgram will exit."


#region ==================== FETCH MASTER JSON

master_json_url = input("Enter master.json url: ")
response = requests.get(master_json_url)
if response.status_code != 200:
    print("\nSomething wrong with the request/response.")
    print(response)
    input(EXIT_MSG)
    sys.exit()
try:
    master_json = response.json()
except:
    print("\nResponse could not be parsed.\n")
    traceback.print_exc()
    input(EXIT_MSG)
    sys.exit()

# endregion


#region ==================== WRITE JSON FILE

master_file = "master.json"
file = open(master_file, "w")
file.write(json.dumps(master_json, indent = 4))
file.close()

#endregion


#region ==================== VIDEO OPTIONS

video_heights = [(i, video['height']) for (i, video) in enumerate(master_json['video'])]
# video_heights = [(0, 540), (1, 240), (2, 360), (3, 1080), (4, 720)]

print("\nVideo choices: ")
for option in video_heights:
    print("%d for %dp" % (option[0], option[1]))
user_video_choice = input("\nEnter your video choice: ")

try:
    user_video_choice = int(user_video_choice)
except:
    print("\nInvalid input: " + user_video_choice)
    input(EXIT_MSG)
    sys.exit()

if user_video_choice < 0 or len(master_json["video"]) - 1 < user_video_choice:
    print("\nInvalid video choice.")
    input(EXIT_MSG)
    sys.exit()

target_video = master_json["video"][user_video_choice]

#endregion


#region ==================== VIDEO DOWNLOAD

video_base_url = master_json_url.split("/sep/video/")[0] + "/sep/video/" + target_video["base_url"]
video_filename = "%s_video_%s.mp4" % (master_json["clip_id"].split("-")[0], target_video["id"])
video_file = open(video_filename, "wb")
video_file.write(base64.b64decode(target_video["init_segment"]))

for video_segment in target_video["segments"]:
    video_segment_url = video_base_url + video_segment["url"]
    print(video_segment_url)
    segment_response = requests.get(video_segment_url, stream=True)
    if segment_response.status_code != 200:
        print("\nSomething went wrong.\n")
        print(segment_url)
        print(segment_response)
        input(EXIT_MSG)
        video_file.flush()
        video_file.close()
        sys.exit()
    for chunk in segment_response:
        video_file.write(chunk)

video_file.flush()
video_file.close()

#endregion


input("\nDONE!")