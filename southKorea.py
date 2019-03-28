#!/usr/bin/env python
# coding=utf8
import csv

from bs4 import BeautifulSoup

readerTmp = open('data/locationData.csv', 'r')
reader = csv.reader(readerTmp, delimiter=",")

svg = open('data/south_korea.svg', 'rt', encoding='UTF8').read()
# svg = open('data/Seoul_districts.svg', 'rt', encoding='UTF8').read()

senior_count = {}
counts_only = []
min_value = 100;
max_value = 0;
past_header = False

for row in reader:
    # if not past_header:
    #     past_header = True
    #     continue

    try:
        unique = row[0]
        count = float(row[1].strip())
        senior_count[unique] = count
        counts_only.append(count)
    except:
        pass

soup = BeautifulSoup(svg, 'html.parser')

paths = soup.findAll('path')

#0부터 농도가 짙음
colors = ["#AD1457", "#C53929", "#F57C00", "#FBC02D", "#689F38", "#088A4B"]

path_style = 'font-size:12px;fill-rule:nonzero;stroke:#000000;stroke-opacity:1;stroke-width:1;stroke-miterlimit:4;stroke-dasharray:none;stroke-linecap:butt;marker-start:none;stroke-linejoin:bevel;fill:'

for p in paths:
    if p['id']:
        try:
            count = senior_count[p['id']]
        except:
            continue
        if count > 4000000:
            color_class = 0
        elif count > 3000000:
            color_class = 1
        elif count > 2000000:
            color_class = 2
        elif count > 1000000:
            color_class = 3
        elif count > 500000:
            color_class = 4
        else:
            color_class = 5

        color = colors[color_class]
        p['style'] = path_style + color
        p['id']=p['id']+" : " + str(int(count))
    else:
        p['id'] = p['id'] + " : 0"



# 메모장에 복사 후 *.sgv 파일로 생성
# 한글 인코딩 문제는 'euc-kr' 설정

f = open('data/test.svg', 'w+', encoding='UTF8')

# print(soup.prettify())

firstLine = True
for i in soup.prettify().split("\n"):
    if firstLine:
        firstLine = False
        continue
    f.write(i + "\n")

f.close()
