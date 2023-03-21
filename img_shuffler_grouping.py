# shuffles image in a folder and regroups them into different folders
# DEST_DIR: the path of images that needs to be processed
# GROUP_SIZE: how many pic in ONE group
# GROUP_NUM: group limit
# DO NOT MAKE ESTIMATED IMAGE NUM MORE THAN ACTUAL IMAGE NUM

import os
import random
from shutil import copyfile

DEST_PATH = "F:\\Documents\\Pictures\\AllTest"

GROUP_SIZE = 26
GROUP_NUM = 11

img_list = []

for root, dirs, files in os.walk(DEST_PATH, topdown=False):
    for file in files:

        if file.endswith(".jpg") or file.endswith(".png"):
            img_list.append(os.path.join(root, file))
        
        random.shuffle(img_list)

        # print(img_list)


for index in range(1, GROUP_NUM + 1):

    if not os.path.exists(os.path.join(DEST_PATH, str(index))):
        os.mkdir(os.path.join(DEST_PATH, str(index)))
    
    for file_i in range(0, GROUP_SIZE):
        try:
            # print("Copying...", file_i * index)
            copyfile(
                os.path.join(
                    DEST_PATH, 
                    img_list[(file_i + int(index - 1 * GROUP_SIZE))]), os.path.join(DEST_PATH, str(index) + '/' + str(file_i) + ".jpg"))
        except IOError as e:
            print("failed \n" + str(e))
            exit(1)
    


