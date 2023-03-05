from PIL import Image
import os

DEST_PATH = "F:\\Documents\\Pictures\\OriRes\\"
REMOVE_ORIGINAL_FILES = False

for root, dirs, files in os.walk(DEST_PATH):

    for d in dirs:

        print("In ", d)

        for file in os.listdir(os.path.join(root, d)):

            file_path = os.path.join(root, d, file)

            if file_path.endswith(".jpg"):

                print("Now Processing......", file_path)

                image = Image.open(file_path)
                image.save(file_path[:-4] + ".png")

                if REMOVE_ORIGINAL_FILES:
                    os.remove(file_path)

