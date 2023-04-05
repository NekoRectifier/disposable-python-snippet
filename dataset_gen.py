import os
import sys
import json_clean
import shutil
from rename import rename

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

    return val_list


def generate(path: str, files: list, is_Val: bool):
    print("Generating sub dataset from folder '%s'" % path)
    folder_name = city_distribution[int(path[-1:])]
    print(int(path[-1:]))
    print(folder_name)

    # if json_switch == 0:
    #     json_clean.main(list)

    # json process
    if not is_Val:
        for index, file in enumerate(files):
            _json_path = join(path, str(index) + ".json")
            _general_name = join(dest_path, "gtFine", "train",
                                 folder_name, folder_name + '_' +
                                 str(index).rjust(6, '0') + '_' + frame_number) + "_gtFine_"

            shutil.copy(
                _json_path,
                _general_name + 'polygons.json'
            )
            # json_clean.removeUnwantedKeysTo(_json_path, _general_name + 'polygons.json')

            shutil.copy(
                join(path, str(index) + ".png"),
                join(dest_path, "leftImg8bit", "train", folder_name,
                     folder_name + str(index).rjust(6, '0') + '_' + frame_number) + '_leftImg8bit.png'
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
        for index, file in enumerate(files):
            _json_path = join(path, str(index) + ".json")
            _general_name = join(dest_path, "gtFine", "val", folder_name,
                                 folder_name + '_' + str(index).rjust(6, '0') + '_' + frame_number) + "_gtFine_"

            shutil.copy(
                _json_path,
                _general_name + 'polygons.json'
            )
            # json_clean.removeUnwantedKeysTo(_json_path, _general_name + 'polygons.json')

            shutil.copy(
                join(path, str(index) + ".png"),
                join(dest_path, "leftImg8bit", "val", folder_name,
                     folder_name + str(index).rjust(6, '0') + '_' + frame_number) + '_leftImg8bit.png'
            )

            json2instanceImg(
                _json_path,
                _general_name + 'instanceIds.png'
            )

            json2labelImg(
                _json_path,
                _general_name + 'labelIds.png'
            )

def preProcessRawFolders(path):
    _index_json = 0
    _index_img = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if str(file).endswith('.json'):
                shutil.copy(join(root, file), join(path, "all_raw", str(_index_json) + ".json"))
                _index_json = _index_json + 1
            elif str(file).endswith('.png'):
                shutil.copy(join(root, file), join(path, "all_raw", str(_index_img) + ".png"))
                _index_img = _index_img + 1


def main(path: str, ratio: float, dest):
    global train_group, val_group
    val_list = []

    # preProcessRawFolders(path=path)

    if os.path.exists(dest):
        shutil.rmtree(dest)

    if not os.path.exists(dest):
        os.mkdir(dest)
    
    for root, dirs, files in os.walk(path, topdown=True):
        # folders name should be numberic and ordered

        for dir in dirs:
            rename(join(root, dir))

        if root == path:
            # print(len(dirs) - 1)
            if not os.path.exists(os.path.join(root, str(len(dirs) - 1))):
                # TODO may have problem here 
                print("Grouping folders number is NOT correspond to its length")
                raise FileExistsError
            else:
                train_group = int(len(dirs) * ratio)
                val_group = len(dirs) - train_group
                print("%d grouping folders detected" % (len(dirs)))
                print(">> %d grouping for train;\n>> %d grouping for validate" % (train_group, val_group))

                val_list = structureCreate(dest, train_group, val_group)
                # photos are randomized before labeling so there's no need for another randomize
        else:
            # sub-folder cycle
            if root in val_list:
                print("val detected")
                generate(root, files, True)
            else:
                generate(root, files, False)


if __name__ == "__main__":
    if len(sys.argv) > 3:
        if type(sys.argv[1]) == str and type(sys.argv[2]) == str and type(sys.argv[3]) == str:
            dest_path = sys.argv[3]
            main(sys.argv[1], float(sys.argv[2]), sys.argv[3])
    else:
        print(
            "ERROR Wrong Exec Format!\nformat:\n    python dataset_gen.py [root_raw_folder] [train/all ratio] [dataset_output_dir]\
                \n\t[root_raw_folder] 是各组以数字命名为子文件夹的根文件夹\t[train/all ratio]是训练/全部图片的比例\t[dataset_output_dir]是输出路径")

