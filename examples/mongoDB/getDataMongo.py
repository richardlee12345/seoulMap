import pymongo
from pymongo import MongoClient
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

epsilon = 1.0
qValue = 1.0 / (math.exp(epsilon) + 1)

portList = [32773, 32769, 32770, 32771, 32772]
fog1Dest = ['1168', '1111', '1114', '1117', '1165']
fog2Dest = ['1121', '1120', '1171', '1123', '1126']
fog3Dest = ['1144', '1129', '1130', '1132', '1135']
fog4Dest = ['1138', '1141', '1150', '1147', '1153']
fog5Dest = ['1154', '1156', '1159', '1162', '1174']

originStatus = {}
noiseStatus = {}

ip='117.16.123.193'

for port in portList:
    # mongoDB 연결
    connection = pymongo.MongoClient(ip, port)

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