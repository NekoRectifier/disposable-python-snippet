import os
import json
import sys

item_list = ["car", "building", "motorcycle",
             "vegetation", "road", "person", "sky", "cone"]


def main(path):
    with open("./output.txt", 'a', encoding='utf-8') as output_f:
        for root, dirs, files in os.walk(path):
            for file in files:
                if str(file).endswith(".json"):

                    with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                        json_data = json.load(f)

                        for object in json_data['objects']: # suitable for jsons processed with json_clean.py
                            if object['label'] not in item_list:

                                _str = "Label problem found: %s\nIn %s\n" % (
                                    object['label'], root + '\\' + file)
                                print(_str)
                                output_f.write(_str)

if __name__ == "__main__":
    if (len(sys.argv) > 1 and len(sys.argv) < 3):
        main(sys.argv[1])
    else:
        print("Wrong command format\nUse: python label_inspect.py [dir]")
