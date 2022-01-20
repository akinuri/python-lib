import sys
import traceback
import requests
import json
from pprint import pprint
import os
import base64


os.system("title " + "Download Laracast Audio")

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


#region ==================== AUDIO OPTIONS

audio_formats = [(i, audio["format"], audio["bitrate"]) for (i, audio) in enumerate(master_json["audio"])]
# audio_formats = [(0, 255000), (1, 128000), (2, 64000), (3, 127000), (4, 75000)]

print("\nAudio choices: ")
for option in audio_formats:
    print("%d for format:%s, bitrate:%s" % (option[0], option[1], option[2]))
user_audio_choice = input("\nEnter your audio choice: ")

try:
    user_audio_choice = int(user_audio_choice)
except:
    print("\nInvalid input: " + user_audio_choice)
    input(EXIT_MSG)
    sys.exit()

if user_audio_choice < 0 or len(master_json["audio"]) - 1 < user_audio_choice:
    print("\nInvalid audio choice.")
    input(EXIT_MSG)
    sys.exit()

target_audio = master_json["audio"][user_audio_choice]

#endregion


#region ==================== AUTIO DOWNLOAD

audio_base_url = master_json_url.split("/sep/video/")[0] +"/"+ target_audio["base_url"].replace("../", "")
audio_filename = "%s_audio_%s.mp4" % (master_json["clip_id"].split("-")[0], target_audio["id"])
audio_file = open(audio_filename, "wb")
audio_file.write(base64.b64decode(target_audio["init_segment"]))

for audio_segment in target_audio["segments"]:
    audio_segment_url = audio_base_url + audio_segment["url"]
    print(audio_segment_url)
    segment_response = requests.get(audio_segment_url, stream=True)
    if segment_response.status_code != 200:
        print("\nSomething went wrong.\n")
        print(segment_url)
        print(segment_response)
        input(EXIT_MSG)
        audio_file.flush()
        audio_file.close()
        sys.exit()
    for chunk in segment_response:
        audio_file.write(chunk)

#endregion


input("\nDONE!")