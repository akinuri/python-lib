import os
import sys
import subprocess
import json
import time
import shutil
from pprint import pprint


os.system("title " + "Getting the changes of the last commit")

EXIT_MSG = "Program will close.\n"


#region ==================== INPUT

if len(sys.argv) == 1:
    print("First argument (input directory path) is missing.")
    input(EXIT_MSG)
    sys.exit()

if not os.path.isdir(sys.argv[1]):
    print("First argument needs to be a directory path.")
    input(EXIT_MSG)
    sys.exit()

#endregion


#region ==================== VARS

git_dir_path  = sys.argv[1]
git_dir_name  = os.path.basename(git_dir_path)
root_dir_path = os.path.dirname(os.path.realpath(__file__))

#endregion


#region ==================== USER CHOICES

GIT_DIFF_UNCOMMITED = 1
GIT_DIFF_STAGED = 2
GIT_DIFF_COMMITED = 3

print("\n".join([
    "What type of diff do you want?",
    "1. Uncommited",
    "2. Staged",
    "3. Commited",
]))

git_diff_choice       = 3
git_diff_choice_input = input("Your choice: ")

try:
    git_diff_choice = int(git_diff_choice_input)
except:
    print(git_diff_choice_input + " is not a valid number.")
    input(EXIT_MSG)
    sys.exit()

if git_diff_choice not in [GIT_DIFF_UNCOMMITED, GIT_DIFF_STAGED, GIT_DIFF_COMMITED]:
    print(git_diff_choice_input + " is not a valid choice.")
    input(EXIT_MSG)
    sys.exit()

git_commit_depth = 1

if git_diff_choice == GIT_DIFF_COMMITED:
    
    git_commit_depth_input = input("Enter the git commit depth: ")
    
    try:
        git_commit_depth = int(git_commit_depth_input)
    except:
        print(git_commit_depth_input + " is not a valid number.")
        input(EXIT_MSG)
        sys.exit()
    
    if git_commit_depth < 1 or git_commit_depth > 30:
        print(str(git_commit_depth) + " seems to exceed the valid commit range.")
        input(EXIT_MSG)
        sys.exit()

#endregion


#region ==================== PRODUCTION IGNORE LIST

git_prod_ignore_file_name = ".prodignore"
git_prod_ignore_list      = []

os.chdir(git_dir_path)

if os.path.isfile(git_prod_ignore_file_name):
    with open(git_prod_ignore_file_name) as file:
        lines = file.readlines()
        git_prod_ignore_list = [line.strip() for line in lines]

#endregion


#region ==================== GET DIFF

git_diff_uncommited = []
git_diff_staged     = ["--staged"]
git_diff_commited   = [
    "HEAD~" + str(git_commit_depth),
    "HEAD"
]
process_args = [
    "git",
    "diff",
    "--name-status",
]

if git_diff_choice == GIT_DIFF_STAGED:
    process_args += git_diff_staged
elif git_diff_choice == GIT_DIFF_COMMITED:
    process_args += git_diff_commited

os.chdir(git_dir_path)
process_result = subprocess.run(
    process_args,
    capture_output=True
)
process_output = process_result.stdout.decode()
os.chdir(root_dir_path)

#endregion


#region ==================== ANALYZE

analysis = {}

process_output_lines = process_output.splitlines()
process_output_lines = [line.split("\t") for line in process_output_lines]

for line in process_output_lines:
    mode, file_path, new_file_path = line + [None] * (3 - len(line))
    score = None
    
    is_file_ignored = False
    for ignore_filter in git_prod_ignore_list:
        target_file = file_path
        if new_file_path is not None:
            target_file = new_file_path
        if target_file.startswith(ignore_filter):
            is_file_ignored = True
            break
    if is_file_ignored:
        continue
        
    if len(mode) != 1:
        score = mode[1:]
        mode = mode[0]
    if mode not in analysis:
        if mode == "R":
            analysis[mode] = {}
        else:
            analysis[mode] = []
    if mode == "R":
        analysis[mode][file_path] = new_file_path
        if "A" not in analysis:
            analysis["A"] = []
        analysis["A"].append(new_file_path)
    else:
        analysis[mode].append(file_path)

analysis_json = json.dumps(analysis, indent=4, sort_keys=True)

#endregion


#region ==================== DUMP

desktop_path         = os.path.join(os.path.expanduser('~'), "Desktop")
dump_dir_path        = os.path.join(desktop_path, git_dir_name)
dump_archive_name    = git_dir_name + ".zip"
dump_archive_path    = os.path.join(desktop_path, dump_archive_name)
delete_previous_dump = None
dump_log_file_name   = "dump.log.json"
dump_log_file_path   = os.path.join(dump_dir_path, dump_log_file_name)

if os.path.isdir(dump_dir_path):
    print("\n".join([
        "There is already a folder named \""+ git_dir_name +"\" in the desktop.",
        "What do you want to do?",
        "0. Nothing (exit)",
        "1. Delete it (continue)",
    ]))
    delete_previous_dump = input("Your choice: ")
    if delete_previous_dump == "0":
        input(EXIT_MSG)
        sys.exit()
    elif delete_previous_dump == "1":
        try:
            shutil.rmtree(dump_dir_path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            input(EXIT_MSG)
            sys.exit()
    else:
        print(delete_previous_dump + " is not a valid answer.")
        input(EXIT_MSG)
        sys.exit()

if (os.path.isfile(dump_archive_path)):
    if delete_previous_dump is None:
        print("There is already an achive named \""+ dump_archive_name +"\" in the desktop.")
        delete_previous_dump = input("Delete it? (Type 0 for no, 1 for yes): ")
    if delete_previous_dump == "0":
        input(EXIT_MSG)
        sys.exit()
    elif delete_previous_dump == "1":
        try:
            os.remove(dump_archive_path)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
            input(EXIT_MSG)
            sys.exit()
    else:
        print(delete_previous_dump + " is not a valid answer.")
        input(EXIT_MSG)
        sys.exit()

os.mkdir(dump_dir_path)

for action, file_paths in analysis.items():
    if action == "M" or action == "A":
        for file_path in file_paths:
            file_dir_path = os.path.join(dump_dir_path, os.path.dirname(file_path))
            if not os.path.isdir(file_dir_path):
                os.makedirs(file_dir_path)
            source_file_path = os.path.join(git_dir_path, file_path)
            dest_file_path   = os.path.join(dump_dir_path, file_path)
            shutil.copy(source_file_path, dest_file_path)

dump_file = open(dump_log_file_path, "w")
dump_file.write(analysis_json)
dump_file.close()

#endregion


#region ==================== ARCHIVE

os.chdir(dump_dir_path)
subprocess.run(
    [
        "zip",
        "-r",
        dump_archive_path,
        "*"
    ],
    stdout=subprocess.DEVNULL
)
os.chdir(root_dir_path)
# os.rename(dump_archive_path, os.path.join(desktop_path, "changes.zip"))

#endregion


print("ALL DONE")

input(EXIT_MSG)
sys.exit()