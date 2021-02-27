import sys
import os
import re

input_file = sys.argv[1]

file_dirname = os.path.dirname(input_file)
file_name    = os.path.basename(input_file).rsplit(".", 1)[0].replace(".Chinese", "")

output_file  = file_dirname + "/" + file_name + ".Clean.srt"

with open(input_file, "r", encoding="utf8") as file:
    lines = file.readlines()
    lines = [line for line in lines if not re.search(u'[\u4e00-\u9fff]', line)]
    
    with open(output_file, "w", encoding="utf8") as the_file:
        the_file.writelines(lines)
    
    
print("Done")

input()
