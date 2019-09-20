import pymongo
from pymongo import MongoClient
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup

epsilon = 1.0
qValue = 1.0 / (math.exp(epsilon) + 1)

portList = [32773, 32769, 32770, 32771, 32772]
fog1Dest = ['1168', '1111', '1114', '1117', '1165']
fog2Dest = ['1121', '1120', '1171', '1123', '1126']
fog3Dest = ['1144', '1129', '1130', '1132', '1135']
fog4Dest = ['1138', '1141', '1150', '1147', '1153']
fog5Dest = ['1154', '1156', '1159', '1162', '1174']

sigungu = {"Seoul_Jongno-gu": 1111,
"Seoul_Jung-gu": 1114,
"Seoul_Yongsan-gu": 1117,
"Seoul_Seongdong-gu": 1120,
"Seoul_Gwangjin-gu": 1121,
"Seoul_Dongdaemun-gu": 1123,
"Seoul_Jungnang-gu": 1126,
"Seoul_Seongbuk-gu": 1129,
"Seoul_Gangbuk-gu": 1130,
"Seoul_Dobong-gu": 1132,
"Seoul_Nowon-gu": 1135,
"Seoul_Eunpyeong-gu": 1138,
"Seoul_Seodaemun-gu": 1141,
"Seoul_Mapo-gu": 1144,
"Seoul_Yangcheon-gu": 1147,
"Seoul_Gangseo-gu": 1150,
"Seoul_Guro-gu": 1153,
"Seoul_Geumcheon-gu": 1154,
"Seoul_Yeongdeungpo-gu": 1156,
"Seoul_Dongjak-gu": 1159,
"Seoul_Gwanak-gu": 1162,
"Seoul_Seocho-gu": 1165,
"Seoul_Gangnam-gu": 1168,
"Seoul_Songpa-gu": 1171,
"Seoul_Gangdong-gu": 1174}

originStatus = {}
noiseStatus = {}

for port in portList:
    # mongoDB 연결
    connection = pymongo.MongoClient('117.16.123.193', port)

    # DB 연결
    taxiDataDB = connection.taxiDataDB

    # Collection 연결
    originCollection = taxiDataDB.origin
    noiseCollection = taxiDataDB.noise

    # originCollection 결과 값 추출
    originResult = originCollection.aggregate([
        {'$group':
            {
                '_id': '$dest',
                'count': {'$sum': 1}
            }
        }
    ])

    # noise 값을 토대로 값을 예측하기 위해 사용되는 변수
    total = 0

    # origin 값 저장 및 total 값 갱신
    for i in originResult:
        originStatus[i['_id']] = i['count']
        total += i['count']

    # noiseCollection 결과 값 추출
    noiseResult = noiseCollection.aggregate([
        {'$group':
            {
                '_id': '$dest',
                'count': {'$sum': 1}
            }
        }
    ])

    # noise 값을 토대로 expect 값 예측
    for i in noiseResult:
        key = i['_id']
        noiseStatus[key] = (i['count'] - total * qValue) / (0.5 - qValue)

print(originStatus)
print(noiseStatus)

# dataFrame 생성
originDataFrame = pd.DataFrame(list(originStatus.items()), columns=['dest','cars'])
noiseDataFrame = pd.DataFrame(list(noiseStatus.items()), columns=['dest','cars'])

# 시각화 하기 위해 추가 col 추가
originDataFrame['index']=0

# dataframe 변형
tmp = originDataFrame.pivot('dest','index','cars')

# heat map 사이즈 조정 및 heat map 테마 설정
plt.figure(figsize=(10,9))
ax = sns.heatmap(tmp, cmap='RdYlGn_r')

# svg 파일로 저장
plt.savefig("data/result/test.svg")

# heatmap svg 파일 읽기
svgFile = open('data/result/test.svg','r')

# BeautifulSoup으로 parser 설정
soup = BeautifulSoup(svgFile,'html')

# 각 구당 데이터 색을 추출하기 위해 select
colorList = soup.select('#QuadMesh_1 > path')

# color={dset:color} 에서 dest에 들어갈 변수들
values = list(sigungu.values())

# 각 구 별 color를 저장할 dict 설정
color={}

# 각 구별 색을 추출하고 color dict에 저장
index=0
for colors in colorList:
    col=colors['style'].split(':')[1].replace(';','')
    dest = values[index]
    color[values[index]]=col
    index+=1



# seoul map svg 파일에 구별로 색을 입히기 위해 파일 read and parser(beautifulSoup)
seoulMapSvg = open('data/origin_svg/Seoul_districts.svg','rt', encoding='UTF8').read()
mapSoup = BeautifulSoup(seoulMapSvg,'html.parser')
paths = mapSoup.find_all('path')

# 기본 path 클래스의 style 구조
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# 각 구별 색을 path데이터에 저장
for p in paths:
    if p['id']:
        col = color[sigungu[p['id']]]
        p['style'] = path_style + col
        p['id']=p['id']+" : " + str(originStatus[str(sigungu[p['id']])])
    else:
        p['id'] = p['id'] + " : 0"

# 변경된 seoul map svg 파일 seaborn 결과 svg 파일에 추가해야 한다.
gTag = mapSoup.find_all('g')

# 기존 출력물을 안보이게 설정
soup.find('g',{'id':'axes_1'})['style']='visibility:hidden'

# 변경된 gTag를 추가
tmp = soup.svg.g
tmp.append(gTag[0])


# output_svg='/home/hp/programs/apache-tomcat-8.5.43/webapps/dataHomepageSpring/resources/data/seoulMap/svg/origin/origin.svg'

# 색을 칠한 seoul map을 저장하기 위해 경로 및 이름 설정
newSeoulMap = open(output_svg, 'w+', encoding='UTF8')
newSeoulMap.write(str(soup))
newSeoulMap.close()

print('finish')
