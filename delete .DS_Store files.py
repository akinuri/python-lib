import glob, os, sys

os.system("title " + "Deleting .DS_Store files")

# ========================= FOLDER DROP

input_path = None

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    print("Drop a folder on me.")
    input()
    sys.exit()

if not os.path.isdir(input_path):
    print("You must ender a folder.")
    input()
    sys.exit()

# ========================= DELETE

i = 0
    
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith('.DS_Store'):
            path = os.path.join(root, file)
            print("Deleting: " + path)
            if os.remove(path):
                print("Unable to delete!")
            else:
                i += 1
                print("Deleted.\n")

print("Files Deleted: " + str(i))

input()