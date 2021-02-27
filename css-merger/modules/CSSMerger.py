import os, sys
import re
import glob

from pprint import pformat

class CSSMerger:
    
    
    input_arguments = None
    input_length    = None
    input_dir       = None
    input_folder    = None
    input_files     = None
    output_file     = None
    output_text     = ""
    
    
    patterns = {
        "line" : {
            "blank" : re.compile(r"^\s*$"),
        },
        "comment" : {
            "line"   : re.compile(r"^ *\/\*.*?\*\/ *$"),
            "inline" : re.compile(r"\/\*.*?\*\/"),
            "block"  : re.compile(r" *\/\*.*?\*\/ *\r?\n?", flags=re.DOTALL),
        },
    }
    
    
    """
    Input should be a folder (that contains CSS files) or a list of CSS files (in a folder).
    Folder name that was passed or the parent folder of the passed CSS files
    will be used as the name of the generated CSS file.
    """
    @classmethod
    def getInput(cls, args):
        cls.input_arguments = args
        cls.input_length    = len(cls.input_arguments)
        
        # make sure there's input
        if cls.input_length == 0:
            print("[Error] No input. Try passing some CSS files to this app.")
            input("\nPress Enter key to exit...")
            sys.exit()
        
        # prevent mixed (file-folder) input
        if cls.input_length != 1:
            for arg in cls.input_arguments:
                if os.path.isdir(arg):
                    print("[Error] Invalid input. You should input either a single folder (that contains CSS files) or just CSS files.")
                    input("\nPress Enter key to exit...")
                    sys.exit()
        
        # input is a folder: find css files
        if cls.input_length == 1 and os.path.isdir(cls.input_arguments[0]):
            cls.input_dir    = cls.input_arguments[0]
            cls.input_folder = os.path.basename(cls.input_dir)
            cls.input_files  = glob.glob(cls.input_dir + "/*.css")
        else:
            # input is a list of files: filter out non-css files
            cls.input_files  = [file for file in cls.input_arguments if os.path.splitext(file)[1][1:].lower() == "css"]
            cls.input_files  = sorted(cls.input_files)
            cls.input_dir    = os.path.dirname(cls.input_files[0])
            cls.input_folder = os.path.basename(cls.input_dir)
        
        cls.input_files = sorted(cls.input_files)
        
        if len(cls.input_files) == 0:
            print("[Error] Empty input. Could not find any CSS files.")
            input("\nPress Enter key to exit...")
            sys.exit()
        
        if len(cls.input_files) == 1:
            print("[Error] Insufficient input. There needs to be more than one file to merge.")
            input("\nPress Enter key to exit...")
            sys.exit()
        
        cls.output_file = cls.input_dir + "\\" + cls.input_folder + ".css"
    
    
    @classmethod
    def dump(cls):
        col_length = len("input_arguments")
        print("input_arguments".ljust(col_length) + " : " + pformat(cls.input_arguments))
        print("input_length".ljust(col_length)    + " : " + str(cls.input_length))
        print("input_dir".ljust(col_length)       + " : " + cls.input_dir)
        print("input_folder".ljust(col_length)    + " : " + cls.input_folder)
        print("input_files".ljust(col_length)     + " : " + pformat(cls.input_files))
        print("output_file".ljust(col_length)     + " : " + cls.output_file)
        print("output_file".ljust(col_length)     + " : " + cls.output_text)
        print("-" * 40)
    
    
    @classmethod
    def processFiles(cls):
        
        all_text = ""
        
        for input_file in cls.input_files:
            
            if input_file == cls.output_file:
                continue
            
            with open(input_file, "r") as file:
                
                lines = file.readlines()
                
                # strip new line char
                lines = [line.rstrip() for line in lines]
                
                # filter out blank lines
                lines = [line for line in lines if not cls.patterns["line"]["blank"].match(line)]
                
                # filter out line comments
                lines = [line for line in lines if not cls.patterns["comment"]["line"].match(line)]
                
                # remove inline comments
                for i, line in enumerate(lines):
                    lines[i] = re.sub(cls.patterns["comment"]["inline"], "", line)
                    # if cls.patterns["comment"]["inline"].search(line):
                    #     print(line, end = "")
                
                # remove block comments
                file_text = "\n".join(lines)
                file_text = re.sub(cls.patterns["comment"]["block"], "", file_text)
                
                if len(all_text) != 0:
                    file_text = "\n" + file_text
                
                all_text += file_text
        
        cls.output_text = all_text
    
    
    @classmethod
    def output(cls):
        file = open(cls.output_file, "w") 
        file.write(cls.output_text) 
        file.close() 