import os
import json

item_list = ["car", "building", "motorcycle", "vegetation", "road", "person", "sky", "cone"]

for root, dirs, files in os.walk("./testdataset"):
    for file in files:
        if str(file).endswith(".json"):

            # with open("./final/gtFine/train/alpha/a.json", 'r', encoding="utf-8") as f:
              with open(os.path.join(root, file)) as f:
                json_data = json.load(f)

                for object in json_data['shapes']:
                    if object['label'] not in item_list:
                        print("problem is %s in file: %s"%(object['label'], file))
