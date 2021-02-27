import os, sys
cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, cwd + "\\modules")

import time
from pprint import pprint

from CSSMerger import *

CSSMerger.getInput(sys.argv[1:])
CSSMerger.processFiles()
# CSSMerger.dump()
CSSMerger.output()

print("Done!")
print("\nExiting in 2 seconds.")
# input()
time.sleep(2)
sys.exit()