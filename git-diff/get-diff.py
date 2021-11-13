import os
import sys
import subprocess
import json
import time
import shutil
from pprint import pprint


os.system("title " + "Getting the changes of the last commit")


#region ==================== OPERATION

OP_LINE_LENGTH = 31
OP_LINE_PAD_CHAR = "."
OP_IGNORE_DELAYS = False
OP_DELAY_MULTIPLIER = 0.5

def print_op(text="", pad=False, end="\n", before_delay=0, after_delay=0, pause=None):
    ignore_delays = "OP_IGNORE_DELAYS" in globals() and OP_IGNORE_DELAYS is True
    delay_multiplier = 1
    if "OP_DELAY_MULTIPLIER" in globals():
        delay_multiplier = OP_DELAY_MULTIPLIER
    if before_delay != 0 and not ignore_delays:
        time.sleep(before_delay * delay_multiplier)
    if text != "":
        if pad is True:
            line_length = len(text)
            if "OP_LINE_LENGTH" in globals():
                line_length = OP_LINE_LENGTH
            pad_char = " "
            if "OP_LINE_PAD_CHAR" in globals():
                pad_char = OP_LINE_PAD_CHAR
            text = text.ljust(line_length, pad_char)
        print(text, end=end)
        if end == "":
            sys.stdout.flush()
    if after_delay != 0 and not ignore_delays:
        time.sleep(after_delay * delay_multiplier)
    if pause == True or type(pause) is str:
        if pause is True:
            pause = ""
        input(pause)

#endregion


#region ==================== ARGUMENT

print_op("Checking arguments", pad=True, end="", before_delay=0.5)

if len(sys.argv) == 1:
    print_op("FAIL", before_delay=0.5, after_delay=0.5)
    print("First argument (input directory path) is missing.")
    input("")
    sys.exit()

if not os.path.isdir(sys.argv[1]):
    print_op("FAIL", before_delay=0.5, after_delay=0.5)
    print("First argument needs to be a directory path.")
    input("")
    sys.exit()

print_op("SUCCESS", before_delay=0.5)

#endregion


#region ==================== VARS

print_op("Creating variables", pad=True, end="", before_delay=0.5)

git_dir_path  = sys.argv[1]
git_dir_name  = os.path.basename(git_dir_path)
root_dir_path = os.path.dirname(os.path.realpath(__file__))

print_op("SUCCESS", before_delay=0.5)

#endregion


# print(sys.argv)
# print(root_dir_path)
# print(output_filename)
# print(output_path)
# input("")


#region ==================== GET DIFF

print_op("Getting git diff", pad=True, end="", before_delay=0.5)

os.chdir(git_dir_path)
result = subprocess.run(
    [
        "git",
        "diff",
        "--name-status",
        "HEAD~1"
    ],
    capture_output=True
)
diff_text = result.stdout.decode()
os.chdir(root_dir_path)

print_op("SUCCESS", before_delay=0.5)

#endregion


#region ==================== DIFF OUTPUT

print_op("Writing the diff to file", pad=True, end="", before_delay=0.5)

diff_filename = "diff-output.txt"
diff_filepath = root_dir_path +"\\" + diff_filename
diff_file = open(diff_filepath, "w")
diff_file.write(diff_text)
diff_file.close()

print_op("SUCCESS", before_delay=0.5)

# print(diff_text)

#endregion


#region ==================== ANALYSIS

print_op("Analyzing the diff", pad=True, end="", before_delay=0.5)

analysis = dict()

lines = diff_text.splitlines()
lines = [line.split("\t") for line in lines]

for line in lines:
    if line[0] not in analysis:
        analysis[line[0]] = list()
    analysis[line[0]].append(line[1])

print_op("SUCCESS", before_delay=0.5)

# pprint(lines)
# pprint(analysis)

#endregion


#region ==================== ANALYSIS OUTPUT

print_op("Writing the analysis to file", pad=True, end="", before_delay=0.5)

analysis_filename = "analysis-output.json"
analysis_filepath = root_dir_path +"\\" + analysis_filename
analysis_file = open(analysis_filepath, "w")
analysis_file.write(json.dumps(analysis, indent=4, sort_keys=True))
analysis_file.close()

print_op("SUCCESS", before_delay=0.5)

#endregion


#region ==================== CHANGE FILES

print_op("Dumping changes", pad=True, end="", before_delay=0.5)

desktop_path = os.path.join(os.path.expanduser('~'), "Desktop")
change_dir_path = os.path.join(desktop_path, git_dir_name)

intervened = False

if os.path.isdir(change_dir_path):
    intervened = True
    print_op("PAUSED", before_delay=0.5)
    print("\nThere is already a folder named \""+ git_dir_name +"\" in the desktop.")
    answer = input("Delete it? (Type 0 for no, 1 for yes): ")
    if answer == "0":
        print_op("\nExiting the program.", before_delay=0.5, after_delay=1)
        sys.exit()
    elif answer == "1":
        try:
            shutil.rmtree(change_dir_path)
        except OSError as e:
            print("\n\nError: %s - %s." % (e.filename, e.strerror))

os.mkdir(change_dir_path)

if intervened:
    print("")
    print_op("Dumping changes", pad=True, end="", before_delay=0.5)

for action, file_paths in analysis.items():
    if action == "M" or action == "A":
        for file_path in file_paths:
            file_dir_path = os.path.join(change_dir_path, os.path.dirname(file_path))
            # print(file_dir_path)
            if not os.path.isdir(file_dir_path):
                os.makedirs(file_dir_path)
            source_file_path = os.path.join(git_dir_path, file_path)
            dest_file_path   = os.path.join(change_dir_path, file_path)
            shutil.copy(source_file_path, dest_file_path)

print_op("SUCCESS", before_delay=0.5)

#endregion


#region ==================== ZIP CHANGE FILES

print_op("Archiving changes", pad=True, end="", before_delay=0.5)

os.chdir(change_dir_path)
print("")
print("")
subprocess.run(
    [
        "zip",
        "-r",
        "../" + git_dir_name + ".zip",
        "*"
    ],
)
os.chdir(root_dir_path)

print("")
print_op("Archiving changes", pad=True, end="", before_delay=0.5)
print_op("SUCCESS", before_delay=0.5)

#endregion


print_op("\nALL DONE", before_delay=0.5, pause="")