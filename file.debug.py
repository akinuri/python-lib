import os
import subprocess
import sys

# When a python script (*.py) encounters an error, the terminal window abruptly closes.
# Running the script from a parent window allows to keep the window open and see the error.

script_path = os.path.abspath(__file__)
script_name = os.path.splitext(os.path.basename(script_path))[0]
script_name = script_name.replace(".debug", "")

try:
    cmd_args = sys.argv[1:]
    cmd = ["python", ("%s.py" % script_name)] + cmd_args
    subprocess.run(cmd, check=True)
except Exception as e:
    print("")
    input("Press any key to exit ... ")

