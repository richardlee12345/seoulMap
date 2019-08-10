import json
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import copy

# 시군구 매칭
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

# svg file(user select data)
userResult = json.load("/home/hp/tomcat/webapps/dataHomepageSpring/resources/data/seoulMap/csv/user/test.json")

# dataFrame 생성
originDataFrame = pd.DataFrame(list(userResult.items()), columns=['dest','cars'])

# 시각화 하기 위해 추가 col 추가
originDataFrame['index']=0

# dataframe 변형
tmp = originDataFrame.pivot('dest','index','cars')

# heat map 사이즈 조정 및 heat map 테마 설정
plt.figure(figsize=(10,9))
ax = sns.heatmap(tmp, cmap='RdYlGn_r')

# svg 파일로 저장
plt.savefig("userTest.svg")

# heatmap svg 파일 읽기
svgFile = open('userTest.svg','r')

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
seoulMapSvg = open('seoulMap.svg','rt', encoding='UTF8').read()
mapSoup = BeautifulSoup(seoulMapSvg,'html.parser')
paths = mapSoup.find_all('path')

# 기본 path 클래스의 style 구조
path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

# 각 구별 색을 path데이터에 저장
for p in paths:
    if p['id']:
        col = color[sigungu[p['id']]]
        p['style'] = path_style + col
        p['id']=p['id']+" : " + str(originResult[str(sigungu[p['id']])])
    else:
        p['id'] = p['id'] + " : 0"

# 변경된 seoul map svg 파일 seaborn 결과 svg 파일에 추가해야 한다.
gTag = mapSoup.find_all('g')

# 기존 출력물을 안보이게 설정
soup.find('g',{'id':'axes_1'})['style']='visibility:hidden'

# 변경된 gTag를 추가
tmp = soup.svg.g
tmp.append(gTag[0])


# 색을 칠한 seoul map을 저장하기 위해 경로 및 이름 설정
newSeoulMap = open('/home/hp/tomcat/webapps/dataHomepageSpring/resources/data/seoulMap/svg/user.svg', 'w+', encoding='UTF8')
newSeoulMap.write(str(soup))
newSeoulMap.close()
