import glob, os, sys
from pprint import pprint


os.system("title " + "Finding the longest file path")


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

path_lengths = {}
longest_path = ""

i = 0

for root, dirs, files in os.walk(input_path):
    for file in files:
        path = os.path.join(root, file)
        path_length = len(path)
        if len(path) > len(longest_path):
            longest_path = path
        if path_length in path_lengths:
            path_lengths[path_length] += 1
        else:
            path_lengths[path_length] = 1
        i += 1

path_lengths = sorted(path_lengths, reverse=True)

print("Longest path:")
print("")
print(longest_path)
print("")
print("Length: " + str(path_lengths[0]))
print("")
print("Files scanned: " + str(i))

#endregion


input("\nPress Enter key to exit...")