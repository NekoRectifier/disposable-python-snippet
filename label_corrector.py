# -- coding: utf-8 --**
import os
import sys
import json

def main(path):
    for root, dirs, files in os.walk(path, True):
        for file in files:
            if str(file).endswith(".json"):
                print(os.path.join(root, file))
                with open(os.path.join(root, file), 'r', encoding="utf-8") as f:
                    
                    json_data = json.load(f)
                    
                    for object in json_data['objects']: # suitable for jsons processed with json_clean.py
                            _label = object['label']
                            if _label == "buliding":
                                object['label'] = "building"
                            elif _label == "motorcycble":
                                object['label'] = "motorcycle"
                            elif _label == "ground":
                                object['label'] = "road"
                            elif _label == "red cone":
                                object['label'] = "cone"
                            elif _label == "blue cone":
                                object['label'] = "cone"
                            elif _label == "yellow cone":
                                object['label'] = "cone"
                            elif _label == "bule cone":
                                object['label'] = "cone"
                            elif _label == "ve1":
                                object['label'] = "vegetation"
                            elif _label == "vegetable":
                                object['label'] = "vegetation"

                with open(os.path.join(root, file), "w+", encoding='utf-8') as f:
                    f.write(json.dumps(json_data, indent=4))

if __name__ == "__main__":
    if (len(sys.argv) > 1 and len(sys.argv) < 3):
        main(sys.argv[1])
    else:
        print("Wrong command format\nUse: python label_inspect.py [dir]")