import glob, os, sys

os.system("title " + "Deleting Thumbs.db files")

# ========================= FOLDER DROP

input_path = None

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    print("Drop a folder on me.")
    input()
    sys.exit()

if not os.path.isdir(input_path):
    print("You must enter a folder.")
    input()
    sys.exit()

# ========================= DELETE

i = 0
    
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file == "Thumbs.db":
            path = os.path.join(root, file)
            os.remove(path)
            print(path)
            i += 1

print("Files Deleted: " + str(i))

input("\nPress Enter key to exit...")