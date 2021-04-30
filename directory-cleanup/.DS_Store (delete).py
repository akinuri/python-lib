import glob, os, sys

os.system("title " + "Deleting .DS_Store files")


#region ==================== INPUT

input_path = None

if len(sys.argv) > 1:
    input_path = sys.argv[1]
else:
    print("Drop a folder on this file.")
    input()
    sys.exit()

if not os.path.isdir(input_path):
    print("You must drop a folder, nothing else.")
    input()
    sys.exit()

#endregion


#region ==================== DELETE

i = 0
    
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file.endswith(".DS_Store"):
            path = os.path.join(root, file)
            os.remove(path)
            print(path)
            i += 1

print("Files deleted: " + str(i))

#endregion


input("\nPress Enter key to exit...")