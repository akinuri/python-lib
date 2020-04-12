import glob, os, sys

from pprint import pprint

os.system("title " + "Deleting ._ files")

# ========================= FOLDER DROP

input_path = None

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    input("Drop a folder on me.")
    sys.exit()

if not os.path.isdir(input_path):
    input("You must enter a folder.")
    sys.exit()

# ========================= DELETE

i = 0
    
for root, dirs, files in os.walk(input_path):
    for filename in files:
        if filename.startswith("._"):
            path = os.path.join(root, filename)
            os.remove(path)
            print(path)
            i += 1

print("Files Deleted: " + str(i))

input("\nPress Enter key to exit...")