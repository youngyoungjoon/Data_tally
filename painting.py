# # Labelme로 작업한 파일들 확인(이미지에 그려주기)

# In[40]:


import cv2
import json
import pandas as pd
import numpy as np
import os

a = pd.read_csv('name_list_with_pixel_value.csv')
b = list(a['name']) #특징 이름값 리스트로 만들기

blue_color = (255, 0, 0)
green_color = (0, 255, 0)
red_color = (0, 0, 255)
white_color = (255, 255, 255)
lavender_color = (255,120, 120)

color_map = [blue_color, green_color, red_color, white_color, lavender_color]

color_dict = dict() #특징별 색깔 지정해주기

i = 0 #name_index
j = 0 #color_index

while i != len(b): # 질병의 특징(키값) = 색깔(값)
    
    color_dict[b[i]] = color_map[j]
    
    j+=1
    
    if j == len(color_map):
        j=0
    i+=1
    
# opencv는 유니코드를 처리하지 못해서 한글로 된 파일을 불러들일 수 없어서 함수 생성

def imread(filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8): #filename = 경로
    try: 
        n = np.fromfile(filename, dtype) 
        #np.fromfile()로 Matlab에서 행렬 데이터를 저장하고 로드하는 것과 같은 효과를 냄
        
        img = cv2.imdecode(n, flags)  # cv2.imdecode( ) 함수를 통해 1D-array인 encoded_img를 3D-array로 만들어줌.
        
        return img 
    
    except Exception as e:
        print(e) 
        return None

def imwrite(filename, img, params=None):  
    try: 
        ext = os.path.splitext(filename)[1] 
        #os.path.splitext 확장자만 따로 분류한다.(리스트로 나타낸다)
        # ex) [('C:\\Users\\young\\FileDetection\\data\\cataract\\cataract_images\\20113019 핑크, OD STT_20190721_153438_DC3_Image_L_003',
            # '.jpg')]  
        result, n = cv2.imencode(ext, img, params) 
        # 이미지를 이미지 파일 스트림으로 다시 인코딩을 한다.
        
        if result: 
            with open(filename, mode='w+b') as f:  #w = 쓰기 b= 바이너리
                n.tofile(f)  #저장
            return True 
        else:
            return False 
        
    except Exception as e:
        print(e) 
        return False

def json_draw(base_path):

    disease_kind = os.listdir(base_path) # 최상위 폴더 불러오기

    for kind in disease_kind:

        dia_list = os.listdir(base_path + '\\' + kind + '\\' + kind +  '_labelme') #각 질병들의 labelme 폴더 불러오기

        for li in dia_list:

            #json파일 로드
            with open(base_path + '\\' + kind + '\\' + kind +  '_labelme\\' + li, 'r', encoding='UTF8') as json_file:   #encoding = 'UTF8'  배열로 불러옴

                json_data = json.load(json_file)

            dict_name = json_data['shapes']

            #파일 존재 확인

            flag = base_path + '\\' + kind + '\\' + kind +  '_images\\' + li[:-4]



            #이미지 opencv로 읽기
            #jpg png 골라서 받기

            if os.path.isfile(flag + 'jpg'):
                #img = cv2.imread(flag + 'jpg', cv2.IMREAD_COLOR)
                img = imread(flag + 'jpg')
            elif os.path.isfile(flag + 'png'):
                #img = cv2.imread(flag + 'png', cv2.IMREAD_COLOR)
                img = imread(flag + 'png')
            elif os.path.isfile(flag + 'tif'):
                #img = cv2.imread(flag + 'tif', cv2.IMREAD_COLOR)
                img = imread(flag + 'tif')
            elif os.path.isfile(flag + 'JPG'):
                #img = cv2.imread(flag + 'JPG', cv2.IMREAD_COLOR)
                img = imread(flag + 'JPG')



            # 선 그리기
            for i in dict_name:

                if i['label'] not in b:

                    print('{}의 특징 이름이 csv에 없습니다.'.format(i['label']))  #특징 이름이 없을때 반복문 종료
                    break

                text = i['label']    #특징 이름
                coordinate = i['points']  #좌표값

                pts = np.array(coordinate, np.int32) #이미지 값은 int값이라 int로 변환
                pts = pts.reshape((-1, 1, 2)) # [[[208, 106]], [[209, 123]], ~~ ] 으로 변환

                cv2.polylines(img, [pts], True, color_dict[text], thickness=3)
                #polylines Parameters:
                #img – image
                #pts (array) – 연결할 꼭지점 좌표
                #isClosed – 닫흰 도형 여부
                #color – Color
                #thickness – 선 두께

                #하나하나씩 line 그려주는건 시간이 오래걸려서 다각형으로 그리기
                #for j in range(1, len(coordinate)):

                    #pt1_x = int(coordinate[j-1][0])
                    #pt1_y = int(coordinate[j-1][1])

                    #pt2_x = int(coordinate[j][0])
                    #pt2_y = int(coordinate[j][1])


                    #cv2.line(img, (pt1_x, pt1_y), (pt2_x, pt2_y), color_dict[text], 3, cv2.LINE_AA)  #line(파일, (시작점_x, 시작점_y), (종료점_x, 종료점_y), 색깔, 선의 개수지정(LINE_AA는 여러개의 선을 그리는 명령어))

                #cv2.line(img, (pt2_x, pt2_y), (int(coordinate[0][0]), int(coordinate[0][1])), color_dict[text], 3, cv2.LINE_AA) #마지막 점을 처음 선과 연결해주기 위해 마지막으로 그려줌

                ########### 추가 ##################
                # frame이라는 이미지에 글씨 넣는 함수
                # frame : 카메라 이미지
                # str : 문자열 변수
                # (0, 100) : 문자열이 표시될 좌표 x = 0, y = 100
                # cv2.FONT_HERSHEY_SCRIPT_SIMPLEX : 폰트 형태
                # 1 : 문자열 크기(scale) 소수점 사용가능
                # (0, 255, 0) : 문자열 색상 (r,g,b)


                if '_' in text:
                    feature_index = text.rfind('_') #특징이름만 찾아주기 위해서 뒤에서부터 찾아주는 rfind 사용
                    feature = text[feature_index+1:]
                else:
                    feature = text


                cv2.putText(img, feature, ( int(coordinate[0][0]), int(coordinate[0][1]) ), cv2.FONT_HERSHEY_SIMPLEX, 1, color_dict[text]) #선의 특징 이름을 이미지에 넣어주기 위해 putText


            if not os.path.isdir(base_path + '\\' + kind +  '\\seg'):  #seg폴더가 없을 때 seg폴더 생성
                os.makedirs(base_path + '\\' + kind + '\\seg')

            #cv2.imwrite('C:\\Users\\young\\_2737476_orig[1]_img.jpg', img)
            #cv2.imwrite(base_path + '\\' + kind + '\\seg\\'+ li[:-4] + 'jpg', img)  # seg폴더에 이미지 저장

            imwrite(base_path + '\\' + kind + '\\seg\\'+ li[:-4] + 'jpg', img)


            #cv2.imshow('image',img)
            #cv2.waitKey(0) #0으로 하면 이미지 창이 무한으로 대기
            #cv2.destroyAllWindows() #화면에 나타난 윈도우를 종료해줌
            





