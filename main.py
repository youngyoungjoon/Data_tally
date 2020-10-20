from painting import *
from bounding_box import *


if __name__ == '__main__':
    bounding_box_cut(r'C:\Users\young\FileDetection\labeling_tally') #이미지 잘라주기
    json_draw(r'C:\Users\young\FileDetection\labeling_tally')  #이미지 역으로 그려주기
