import os
import json
import sys

def main(target):

    print(type(target))
    print(type("str"))

    try:
        if type(target) == type("sad"):
            for root, dirs, files in os.walk(target):
                for file in files:
                    if str(file).endswith(".json"):
                        removeUnwantedKeys(os.path.join(root, file))
        elif type(target) == type(list):
            for path in target:
                if os.path.exists(path=path) and str(path).endswith(".json"):
                    removeUnwantedKeys(path)
                else:
                    print("list path error")
                    raise FileNotFoundError
        else:
            raise ValueError
    finally:
        pass


def removeUnwantedKeys(abs_path):
    with open(abs_path, "r", encoding="utf-8") as file_handle:
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
        
    with open(abs_path, 'w+', newline='\n') as f:
        f.write(json.dumps(json_data, indent=4, sort_keys=True))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("needs a path arg points to dir of jsons")
    elif len(sys.argv) == 2:
        if os.path.exists(sys.argv[1]):
            print("WARNING: This program modifies json file itself")
            print("Processing...")
            main(sys.argv[1])
        else:
            raise FileNotFoundError