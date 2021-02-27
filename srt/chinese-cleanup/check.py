import sys
import os
import re
import time

input_file = sys.argv[1]

with open(input_file, "r", encoding="utf8") as file:
    lines = file.readlines()
    
    # https://stackoverflow.com/a/34587623/2202732
    for line in lines:
        if re.search(u'[\u4e00-\u9fff]', line):
            time.sleep(0.025)
            print(line)

print("Done")

input()
