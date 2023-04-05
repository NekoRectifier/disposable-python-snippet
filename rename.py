import os
import shutil

def rename(folder_path):
    # step 1: traverse all files in the folder
    print(folder_path)
    png_dict = {}
    json_dict = {}
    for file in os.listdir(folder_path):
        # check if it is a png or json file
        if file.endswith(".png"):
            # get the number in the file name
            num = int(os.path.splitext(file)[0])
            # store the file name and number in a dictionary
            png_dict[num] = file
        elif file.endswith(".json"):
            # get the number in the file name
            num = int(os.path.splitext(file)[0])
            # store the file name and number in a dictionary
            json_dict[num] = file

    # step 2: sort the dictionary by number
    sorted_png_dict = dict(sorted(png_dict.items()))
    sorted_json_dict = dict(sorted(json_dict.items()))

    # step 3: rename the files
    for i, key in enumerate(sorted_png_dict.keys()):
        old_png_name = sorted_png_dict[key]
        old_json_name = sorted_json_dict[key]
        new_png_name = str(i) + os.path.splitext(old_png_name)[1]
        new_json_name = str(i) + os.path.splitext(old_json_name)[1]
        # rename the png and json files together
        shutil.move(os.path.join(folder_path, old_png_name), os.path.join(folder_path, new_png_name))
        shutil.move(os.path.join(folder_path, old_json_name), os.path.join(folder_path, new_json_name))