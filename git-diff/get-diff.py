import os
import sys
import subprocess
import json
import time
from pprint import pprint


os.system("title " + "Getting the changes of the last commit")


#region ==================== OPERATION

OP_LINE_LENGTH = 31
OP_LINE_PAD = "."
OP_IGNORE_DELAYS = True

def print_op(text="", pad=False, end="\n", flush=False, before_delay=0, after_delay=0, wait=None):
    ignore_delays = "OP_IGNORE_DELAYS" in globals() and OP_IGNORE_DELAYS is True
    if before_delay != 0 and not ignore_delays:
        time.sleep(before_delay)
    if text != "":
        if pad is True:
            if "OP_LINE_LENGTH" in globals():
                line_pad = " "
                if "OP_LINE_PAD" in globals():
                    line_pad = OP_LINE_PAD
                text = text.ljust(OP_LINE_LENGTH, line_pad)
        print(text, end=end)
        if flush:
            sys.stdout.flush()
    if after_delay != 0 and not ignore_delays:
        time.sleep(after_delay)
    if wait == True or type(wait) is str:
        if wait is True:
            wait = ""
        input(wait)

#endregion


#region ==================== ARGUMENT

print_op("Checking arguments", True, "", True, 0.5)

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

print_op("Creating variables", True, "", True, 0.5)

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

print_op("Getting git diff", True, "", True, 0.5)

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

print_op("Writing the diff to file", True, "", True, 0.5)

diff_filename = "diff-output.txt"
diff_filepath = root_dir_path +"\\" + diff_filename
diff_file = open(diff_filepath, "w")
diff_file.write(diff_text)
diff_file.close()

print_op("SUCCESS", before_delay=0.5)

# print(diff_text)

#endregion


#region ==================== ANALYSIS

print_op("Analyzing the diff", True, "", True, 0.5)

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

print_op("Writing the analysis to file", True, "", True, 0.5)

analysis_filename = "analysis-output.json"
analysis_filepath = root_dir_path +"\\" + analysis_filename
analysis_file = open(analysis_filepath, "w")
analysis_file.write(json.dumps(analysis, indent=4, sort_keys=True))
analysis_file.close()

print_op("SUCCESS", before_delay=0.5)

#endregion


print_op("ALL DONE", before_delay=0.5, wait="")