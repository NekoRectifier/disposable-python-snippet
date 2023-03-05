import os
import random
from shutil import copyfile

DEST_PATH = "F:\\Documents\\Pictures\\AllTest"

GROUP_SIZE = 26
GROUP_NUM = 1

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
            copyfile(os.path.join(DEST_PATH, img_list[file_i * index]), os.path.join(DEST_PATH, str(index) + '/' + str(file_i) + ".jpg"))
        except IOError as e:
            print("failed \n" + str(e))
            exit(1)
    


