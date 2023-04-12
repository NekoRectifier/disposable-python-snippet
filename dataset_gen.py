import os
import sys
import json
import shutil
import argparse

from cityscapesscripts.preparation.json2instanceImg import json2instanceImg
from cityscapesscripts.preparation.json2labelImg import json2labelImg

join = os.path.join
city_distribution = ['alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot', 'golf', 'hotel', 'india',
                     'juliett', 'kilo', 'lima', 'mike', 'november', 'oscar', 'papa', 'quebec', 'romeo',
                     'sierra', 'tango', 'uniform', 'victor', 'whiskey', 'xray', 'yankee', 'zulu']
# train folder names goes from start and val foolder names goes backwards

# GLOBALS

train_group = 0
val_group = 0
dest_path = ""

json_switch = 0
frame_number = "000016"

data = {}

""" 
This function renames irregular numeric names due to manully removing unwanted labeling jsons and images into regular form.

Args:
folder_path -- receives a path that you designate
"""
def rearrange(folder_path):
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


"""
Creates initial dataset folders structure

Args:
dest_path -- your target path for creating the dataset
train -- numbers of folders that included in "train" group
val -- numbers of folders that included in "val" group
"""

def structureCreate(dest_path: str, train: int, val: int):
    # build basic cityscape like folder structure 
    for _path in [join(dest_path, "gtFine"), join(dest_path, "leftImg8bit")]:
        os.mkdir(_path)

        os.mkdir(join(_path, "train"))
        os.mkdir(join(_path, "val"))

    train_list = city_distribution[:train]
    val_list = city_distribution[-val:]

    for _train in train_list:
        os.mkdir(join(dest_path, "gtFine", "train", _train))
        os.mkdir(join(dest_path, "leftImg8bit", "train", _train))

    for _val in val_list:
        os.mkdir(join(dest_path, "gtFine", "val", _val))
        os.mkdir(join(dest_path, "leftImg8bit", "val", _val))

"""
Check json keys one by one then modify and finally save it to designated path.

Args:
json_path -- path to original json file
output_path -- path to 
"""
def jsonProcess(json_path, output_path):
    print("Handling %s")
    with open(json_path, "r", encoding="utf-8") as file_handle:
        json_data = json.load(file_handle)

        json_data.pop('imageData')
        json_data.pop('flags')
        json_data.pop('imagePath')
        json_data.pop('version')

        json_data['imgWidth'] = json_data.pop('imageWidth')
        json_data['imgHeight'] = json_data.pop('imageHeight')
        json_data['objects'] = json_data.pop('shapes')
        objs = json_data['objects']

        for obj in objs:
            obj.pop('flags')
            obj.pop('group_id')
            obj.pop('shape_type')

            obj['polygon'] = obj.pop('points')
            for point in obj['polygon']:
                point[0] = int(point[0])
                point[1] = int(point[1])

    with open(output_path, 'w', encoding='utf-8', newline="\n") as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))


def generate(path: str, files: list):
    print("Generating sub dataset from folder '%s'" % path)

    if str(path[path.rfind('\\') + 1:]).isdigit():
        index = int(path[path.rfind('\\') + 1:])
        # Windows
    else:
        index = int(path[path.rfind('/') + 1:])
        # Linux
    # original folder naming number

    if index < train_group:
        print("designated to train")

        folder_name = city_distribution[index]

        for index in range(0, int(len(files)/2)):
            _json_path = join(path, str(index) + ".json")
            _general_name = join(dest_path, "gtFine", "train",
                                 folder_name, folder_name + '_' +
                                 str(index).rjust(6, '0') + '_' + frame_number) + "_gtFine_"

            shutil.copy(
                _json_path,
                _general_name + 'polygons.json'
            )
            

            shutil.copy(
                join(path, str(index) + ".png"),
                join(dest_path, "leftImg8bit", "train", folder_name,
                     folder_name + '_' + str(index).rjust(6, '0') + '_' + frame_number) + '_leftImg8bit.png'
            )

            json2labelImg(
                _general_name + 'polygons.json',
                _general_name + 'labelTrainIds.png',
                "trainIds"
            )

            json2instanceImg(
                _general_name + 'polygons.json',
                _general_name + 'instanceIds.png'
            )

            json2labelImg(
                _general_name + 'polygons.json',
                _general_name + 'labelIds.png'
            )
    else:
        print("designated to val")

        folder_name = city_distribution[-(index-train_group + 1)]

        for index in range(0, int(len(files)/2)):
            _json_path = join(path, str(index) + ".json")
            _general_name = join(dest_path, "gtFine", "val",
                                folder_name, folder_name + '_' + 
                                str(index).rjust(6, '0') + '_' + frame_number) + "_gtFine_"

            shutil.copy(
                _json_path,
                _general_name + 'polygons.json'
            )
            
            # json_clean.removeUnwantedKeysTo(_json_path, _general_name + 'polygons.json')

            shutil.copy(
                join(path, str(index) + ".png"),
                join(dest_path, "leftImg8bit", "val", folder_name,
                     folder_name + '_' + str(index).rjust(6, '0') + '_' + frame_number) + '_leftImg8bit.png'
            )

            json2labelImg(
                _general_name + 'polygons.json',
                _general_name + 'labelTrainIds.png',
                "trainIds"
            )

            json2instanceImg(
                _general_name + 'polygons.json',
                _general_name + 'instanceIds.png'
            )

            json2labelImg(
                _general_name + 'polygons.json',
                _general_name + 'labelIds.png'
            )


def main(path: str, ratio: float, dest):
    global train_group, val_group

    if os.path.exists(dest):
        shutil.rmtree(dest)
    # remove provious gernerated datasets

    if not os.path.exists(dest):
        os.mkdir(dest)
    
    for root, dirs, files in os.walk(path, topdown=True):
        # folders name should be numberic and ordered

        for dir in dirs:
            rearrange(join(root, dir))
            #TODO manully controled

        if root == path:
            # print(len(dirs) - 1)
            if not os.path.exists(os.path.join(root, str(len(dirs) - 1))):
                # TODO may have problem here 
                print("Not enough folder while trying to correspond number with them.")
                raise FileNotFoundError
            else:
                train_group = int(len(dirs) * ratio)
                val_group = len(dirs) - train_group
                print("%d grouping folders detected" % (len(dirs)))
                print(">> %d grouping for train;\n>> %d grouping for validate" % (train_group, val_group))

                structureCreate(dest, train_group, val_group)
                
                # photos are randomized before labeling so there's no need for another randomize
        else:
            # sub-folder cycle
            generate(root, files)


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Gernerate a fully usable cityscapes-like dataset")
    parser.add_argument("--source", type=str, help="path to raw root folder", required=True)
    parser.add_argument("-r", "--ratio", type=float, help="ratio of train folders to all folders", required=False, default=0.8)
    parser.add_argument("-o", "--output", type=str, help="output path", required=False, default="./out")
    parser.add_argument("--no-json-process", type=bool, help="control whether or not to process json files", default=False, required=False)

    args = parser.parse_args()

    # if len(sys.argv) > 3:
    #     if type(sys.argv[1]) == str and type(sys.argv[2]) == str and type(sys.argv[3]) == str:
    #         dest_path = sys.argv[3]
    #         main(sys.argv[1], float(sys.argv[2]), sys.argv[3])
    # else:
    #     print(
    #         "format:\n    python dataset_gen.py [root_raw_folder] [train/all ratio] [dataset_output_dir]\
    #             \n\t[root_raw_folder] 是各组以数字命名为子文件夹的根文件夹\t[train/all ratio]是训练/全部图片的比例\t[dataset_output_dir]是输出路径")

# TODO 添加一参数位用于手动控制json情况

"""
Before using you MUST modify labels.py in cityscapesscript in order to create the dataset successfully. 
You MAY learn how to do that in <https://huat-fsac.eu.org/docs/%E6%97%A0%E4%BA%BA%E7%B3%BB%E7%BB%9F%E9%83%A8/%E6%84%9F%E7%9F%A5%E7%BB%84/dataset-generating/>
"""

#TODO
#1. json clean 还未完全处理
#
#
#
