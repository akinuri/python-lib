import sys
import os
import re
import srt
from pprint import pprint 

input_file = sys.argv[1]

file_dirname = os.path.dirname(input_file)
file_name    = os.path.basename(input_file).rsplit(".", 1)[0].replace(".Chinese", "")

output_file  = file_dirname + "/" + file_name + ".Clean.srt"


"""
 * Remove Chinese lines     => "电波诚译"
 * Remove wandering b tag   => "^</b>$"
 * Remove trailing b tag    => "^foo</b>$"
 * Remove empty lines       => "^foo\n\nbar$"
 * Remove duplicate subtitles
"""


with open(input_file, "r", encoding="utf8") as file:
    content   = file.read()
    subtitles = list(srt.parse(content))
    
    # """
    
    # First Pass: Remove Chinese lines
    for subtitle in subtitles:
        lines = subtitle.content.split("\n")
        # detect
        # for line in lines:
            # if re.search(u'[\u4e00-\u9fff]', line):
                # print(subtitle.index)
                # print(line)
        # remove
        lines = [line for line in lines if not re.search(u'[\u4e00-\u9fff]', line)]
        subtitle.content = "\n".join(lines)
        # print(lines)
    
    
    # Second Pass: Remove wandering </b> tag
    for subtitle in subtitles:
        lines = subtitle.content.split("\n")
        # detect
        # if re.search("^</b>$", line):
            # pprint(subtitle.index)
            # pprint(lines)
        # remove
        lines = [line for line in lines if not re.search("^</b>$", line)]
        subtitle.content = "\n".join(lines)
        # print(lines)
    
    
    # Third Pass: Remove trailing </b> tag
    for subtitle in subtitles:
        lines = subtitle.content.split("\n")
        # detect
        # if "</b>" in line:
            # pprint(subtitle.index)
            # pprint(lines)
        # remove
        lines = [line.replace("</b>", "") if "</b>" in line else line for line in lines]
        subtitle.content = "\n".join(lines)
        # print(lines)
    
    
    # Fourth Pass: Remove trailing </b> tag
    for subtitle in subtitles:
        lines = subtitle.content.split("\n")
        # detect
        # if line == "":
            # pprint(subtitle.index)
            # pprint(lines)
        # remove
        lines = [line for line in lines if line != ""]
        subtitle.content = "\n".join(lines)
        # print(lines)
    
    # """
    
    
    # Fifth Pass: Remove duplicate subtitles
    
    content   = srt.compose(subtitles)
    subtitles = list(srt.parse(content))
    
    originals  = {}
    duplicates = []
    
    last_subtitle = None
    
    for subtitle in subtitles:
        if last_subtitle:
            if last_subtitle.content == subtitle.content:
                duplicates.append(subtitle.index)
                if subtitle.content in originals:
                    originals[subtitle.content].end = subtitle.end
                else:
                    originals[last_subtitle.content] = last_subtitle
                    last_subtitle.end = subtitle.end
        last_subtitle = subtitle
    
    # pprint(duplicates)
    
    subtitles = [subtitle for subtitle in subtitles if subtitle.index not in duplicates]
    
    # """
    
    content = srt.compose(subtitles)
    
    with open(output_file, "w", encoding="utf8") as the_file:
        the_file.writelines(content)
    
    # """
    

print("Done")

input()
