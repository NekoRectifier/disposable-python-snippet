import os
from shutil import copyfile

DEST_DIR_ALL = "F:\\Documents\\Pictures\\AllOriginal"

f_list_1 = os.listdir("F:\\Documents\\Pictures\\OriRes")
f_list_2 = os.listdir("F:\\Documents\\Pictures\\HiRes")

f_list_1.extend(f_list_2)

f_list_all = os.listdir("F:\\Documents\\Pictures\\AllOriginal")

desel_list = list(set(f_list_1) ^ set(f_list_all))

print(desel_list)