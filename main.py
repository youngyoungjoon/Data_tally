from painting import *
from bounding_box import *

def all_main(base_path):
    bounding_box_cut(base_path) #이미지 xml(bounding_box)좌표로 잘르기
    json_draw(base_path)        #이미지에 json(labelme) 좌표로 그려기


if __name__ == '__main__':

    all_main(r'C:\Users\young\FileDetection\labeling_tally')

