import os
from PIL import Image

DEST_DIR = "F:\\Documents\\Pictures\\AllTest"
S_WIDTH = 1920
S_HEIGHT = 1080
S_RATIO = S_WIDTH / S_HEIGHT

def process_dir(_dir):
    for file in os.listdir(_dir):
        if file.endswith('.jpg'):
            print("Processing : ", file)

            t_img = Image.open(os.path.join(_dir, file))
            _width, _height = t_img.size
            _ratio = _width / _height

            print("width:", _width, "height:", _height)

            if _width == S_WIDTH and _height == S_HEIGHT:
                continue
            
            new_img = Image.new(t_img.mode, (S_WIDTH, S_HEIGHT), (0, 0, 0))

            if _ratio == S_RATIO:
                # 等比缩放
                new_img = t_img.resize((S_WIDTH, S_HEIGHT))

            elif _ratio > S_RATIO:
                new_height = int((abs(S_WIDTH-_width)/_width) * _height + _height)
                t_img = t_img.resize((S_WIDTH, new_height))
                new_img.paste(t_img, (0, int((S_HEIGHT - new_height) / 2)))

            elif _ratio < S_RATIO:
                new_width = int(((abs(S_HEIGHT-_height) / _height) * _width) + _width)
                t_img = t_img.resize((new_width, S_HEIGHT))
                new_img.paste(t_img, (int((S_WIDTH-new_width)/2), 0))

            else:
                print('asddsa')

            # new_img.show()
            new_img.save(os.path.join(_dir, file[:-4] + '.png'))

def del_other_files(_dir):
    for file in os.listdir(_dir):
        if file.endswith('.jpg'):
            os.remove(os.path.join(_dir, file))


if __name__ == "__main__":
    for root, dirs, files in os.walk(DEST_DIR):
        for dir in dirs:
            _path = os.path.join(root, dir)
            print("Processing Dir: ", _path)
            # process_dir(_path)
            del_other_files(_path)
