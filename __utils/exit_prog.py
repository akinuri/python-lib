import sys

def exit_prog(*messages):
    for message in messages:
        print(message)
        if message != "":
            print("")
    print("Program will close.")
    input("")
    sys.exit()