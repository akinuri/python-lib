import glob, os, sys

os.system("title " + "Finding Thumbs.db files")


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


#region ==================== FIND

i = 0
    
for root, dirs, files in os.walk(input_path):
    for file in files:
        if file == "Thumbs.db":
            i += 1

print("Files found: " + str(i))

#endregion


input("\nPress Enter key to exit...")