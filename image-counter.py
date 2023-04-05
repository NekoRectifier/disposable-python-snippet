import os
import sys

counter = 0

def main(path):
    global counter
    for root, dirs, files in os.walk(path, topdown=True):
        for file in files:
            if(str(file).endswith(".png")):
                counter = counter + 1
    
    print(counter)

if __name__ == "__main__":
    if (len(sys.argv) > 1 and len(sys.argv) < 3):
        main(sys.argv[1])
    else:
        print("Wrong command format\nUse: python label_inspect.py [dir]")