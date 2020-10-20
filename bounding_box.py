from PIL import Image
import xml.etree.ElementTree as elemTree  # xml 객체화
import os


def bounding_box_cut(path):
    # path = 'C:\\Users\\young\\real_demo' 질병 이미지 데이터 경로

    base_path = os.listdir(path)

    for i in base_path:

        original_img = os.listdir(path + '\\' + i + '\\' + i + '_images')  #
        # xml_img = os.listdir('C:\\Users\\young\\demo_version\\' + i +'\\' + i + '_labelimg')

        number = 0
        for j in original_img:

            if j[-3:] == 'jpg':
                b = j[:-3] + 'xml'

                if b not in os.listdir(path + '\\' + i + '\\' + i + '_labelimg'):  # 원본 이미지 경우 xml개수가 안맞아서 조건문추가
                    continue

                img = Image.open(path + '\\' + i + '\\' + i + '_images' + '\\' + j).convert('RGB')
                tree = elemTree.parse(path + '\\' + i + '\\' + i + '_labelimg' + '\\' + b)
                objs = tree.getroot().findall('object')


            else:  # jpg 외 다른 확장자 파일은 에러가 발생해서 jpg로 변환한 다음 작업

                a = j[:-3] + 'jpg'

                b = j[:-3] + 'xml'

                if b not in os.listdir(path + '\\' + i + '\\' + i + '_labelimg'):
                    continue

                img = Image.open(path + '\\' + i + '\\' + i + '_images' + '\\' + j).convert('RGB').save(
                    path + '\\' + i + '\\' + i + '_images' + '\\' + a, 'jpeg')
                os.remove(path + '\\' + i + '\\' + i + '_images' + '\\' + j) #기존 확장자 삭제
                tree = elemTree.parse(path + '\\' + i + '\\' + i + '_labelimg' + '\\' + b)
                objs = tree.getroot().findall('object')

            for obj in objs:
                bbox = obj.find('bndbox')  # 특정 attrib의 특정 값을 가진 태그 가져오는 방법
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
                a = (xmin, ymin, xmax, ymax)
                crop_img = img.crop(a)

                if not os.path.isdir(path + '\\' + i + '\\img'):
                    os.makedirs(path + '\\' + i + '\\img', 0o777)

                crop_img.save(path + '\\' + i + '\\img\\' + '{}(crop){}.jpg'.format(j[:-4], number))

                number += 1