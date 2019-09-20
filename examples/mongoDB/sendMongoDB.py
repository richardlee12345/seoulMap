import math
import pymongo
import random
import time

# 기능
# 카프카 토픽에 접근하여 데이터를 받는다.
# 1.데이터 토픽에 따라 맞는 포트를 찾는다. (함수 작성 parm : data)
#  1-1. data를 받고 ,로 split
#    1-1-1. 데이터의 dest로 fogPort를 찾는다.
#  1-2. 원본 데이터 mongodb에 저장
#  1-3. 원본 데이터에 노이즈 추가 (함수 작성)
#  1-4. 노이즈데이터 mongodb에 저장
# 2. 원본데이터와 노이즈 데이터를 만들고 mongoDB에 저장

taxi_data='data/taxi_data/taxiData.csv'
epsilon = 1.0;
qValue = 1 / (math.exp(epsilon) + 1);
pValue = 0.5;

ip='117.16.123.194'

fogPort = [32773, 32769, 32770, 32771, 32772]
fogNode = {
    32773: ["1168", "1111", "1114", "1117", "1165"],
    32769: ["1121", "1120", "1171", "1123", "1126"],
    32770: ["1144", "1129", "1130", "1132", "1135"],
    32771: ["1138", "1141", "1150", "1147", "1153"],
    32772: ["1154", "1156", "1159", "1162", "1174"],
}

connection1 = pymongo.MongoClient('117.16.123.193', 32773)
connection2 = pymongo.MongoClient('117.16.123.193', 32769)
connection3 = pymongo.MongoClient('117.16.123.193', 32770)
connection4 = pymongo.MongoClient('117.16.123.193', 32771)
connection5 = pymongo.MongoClient('117.16.123.193', 32772)

connectionList = [connection1, connection2, connection3, connection4, connection5]


def viewMongo():
    for connection in connectionList:
        print(connection)
        originDB = connection.originDB
        noiseDB = connection.noiseDB

        originCollection = originDB.taxiData
        noiseCollection = noiseDB.taxiData

        result = originCollection.find()
        print('origin', result.count())
        #         for i in result:
        #             print(i)

        result = noiseCollection.find()
        print('noise', result.count())
        #         for i in result:
        #             print(i)
        print()


def getFogPort(dest):
    for port in fogNode.keys():
        if (dest in fogNode[port]):
            #             print(fogNode[port].index(dest), port)
            return fogNode[port].index(dest), port


def getConnection(port):
    return connectionList[fogPort.index(port)]


def addNoise(index):
    bitMask = []
    for i in range(5):
        if (i == index):
            bitMask.append("1")
        else:
            bitMask.append("0")

    for i in range(5):
        randomNum = random.random()
        if (bitMask[i] == "0"):
            if (randomNum <= qValue):
                bitMask[i] = "1"
            else:
                bitMask[i] = "0"
        else:
            if (randomNum <= pValue):
                bitMask[i] = "1"
            else:
                bitMask[i] = "0"
    return bitMask


def addMongo(dic, collection):
    collection.insert_one(dic)


def addDataToMongo(data):
    outSeoul = False
    try:
        index, port = getFogPort(data[3])
    except:
        outSeoul = True
    if (outSeoul): return

    connection = getConnection(port)

    taxiDataDB = connection.taxiDataDB

    #     originDB = connection.originDB
    #     noiseDB = connection.noiseDB

    originCollection = taxiDataDB.origin
    noiseCollection = taxiDataDB.noise

    #     originCollection = originDB.taxiData
    #     noiseCollection = noiseDB.taxiData

    dicTmp = {
        "id": data[0],
        "day": data[1],
        "time": data[2],
        "dest": data[3]
    }

    # insert data to origin
    originCollection.insert_one(dicTmp)
    #     addMongo(dicTmp,originCollection)

    # make noise data
    noiseBitMask = addNoise(index)
    #     dicTmp ={
    #         "id" : data[0],
    #         "day" : data[1],
    #         "time" : data[2],
    #         "dest" : data[3]
    #     }

    for i in range(len(noiseBitMask)):
        if noiseBitMask[i] == "1":
            key = fogNode[port][i]
            noiseDicTmp = {
                "id": data[0],
                "day": data[1],
                "time": data[2],
                "dest": key
            }
            noiseCollection.insert_one(noiseDicTmp)

        #     for index in range(len(fogNode[port])):


#         dicTmp[fogNode[port][index]]=noiseBitMask[index]

#     addMongo(dicTmp,noiseCollection)

def init():
    for port in fogNode.keys():
        connection = pymongo.MongoClient(ip, port)
        print(connection)
        connection.drop_database("originDB")
        connection.drop_database("noiseDB")


init()
file = open(taxi_data, 'r')
firstLine = True
while True:
    line = file.readline().strip()
    #     print(line)
    if (firstLine):
        firstLine = False
        continue
    data = line.split(',')
    addDataToMongo(data)
file.close()

print('finish')
viewMongo()
