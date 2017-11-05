#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

url = 'http://client1.aipao.me/api/token/QM_Users/Login'


def GetToken(url, datas, auth):
    headers = {'Host': 'client1.aipao.me', 'Connection': 'keep-alive', 'Accept': '*/*', 'Version': 'B2.612',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'auth': auth}
    response = requests.get(url, params=datas, headers=headers)
    json = response.json()
    print('\nTry getting token...Success: ' + str(json['Success']))
    if json['Success']:
        print('Token: ' + json['Data']['Token'])
        return json['Data']['Token']
    else:
        return 'failed'


def imei2json(imei):
    return {'IMEICode': imei}


def encode(x):
    if x == '0':
        return 'p'
    if x == '1':
        return 'q'
    if x == '2':
        return 'w'
    if x == '3':
        return 'e'
    if x == '4':
        return 'r'
    if x == '5':
        return 't'
    if x == '6':
        return 'y'
    if x == '7':
        return 'u'
    if x == '8':
        return 'i'
    if x == '9':
        return 'o'


def code2field(fieldcode):
    gy = ['30.544342', '114.366888']  # 桂园田径场
    ac = ['30.545102', '114.372494']  # 九一二操场
    gc = ['30.549832', '114.374182']  # 工学部体育场
    xc = ['30.534084', '114.367382']  # 信息学部竹园田径场
    yxb = ['30.561585', '114.359509']  # 医学部杏林田径场
    if fieldcode == '1':
        return gy
    if fieldcode == '2':
        return ac
    if fieldcode == '3':
        return gc
    if fieldcode == '4':
        return xc
    if fieldcode == '5':
        return yxb


def StartRunning(Token, field):
    headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
    datas = {'Lat': field[0], 'Lng': field[1], 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
             'Level_Length': '2000', 'IsSchool': '1'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/startRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print('\nTry getting RunId...Success: ' + str(json['Success']))
    if json['Success']:
        print('RunId: ' + json['Data']['RunId'])
        return json['Data']['RunId']
    else:
        return 'failed'


def StopRunning(Token, RunId, timecode, distancecode, stepnumcode, auth):
    headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0', 'Accept-Language': 'zh-cn',
               'auth': auth, 'Connection': 'keep-alive'}
    datas = {'S1': RunId, 'S2': 'tppp', 'S3': 'qooy', 'S4': timecode, 'S5': distancecode, 'S6': '', 'S7': '1',
             'S8': 'pqwertyuio', 'S9': stepnumcode}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/EndRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print('\nrequestURL: ' + requestURL)
    print(json)
    if json['Success']:
        print('\n跑步数据成功上传')
    else:
        print('\n跑步数据上传失败，请重试')
    return json


imei = input('\nIMEI code: ')
if imei == 'default':
    imei = '766032a7ce6f4df2abc499bb2b79ecd0'
elif imei == 'xzz':
    imei = 'cb943d6fddef4f6892746b9d02a51d48'
auth = input('auth: ')
fieldcode = input('选择场地(1.桂园田径场 2.九一二操场 3.工学部体育场 4.信息学部竹园田径场 5.医学部杏林田径场): ')
field = code2field(fieldcode)
runningData = []
codedData = {'time': '900', 'distance': '2000'}
runningData.append(input('跑步时间（秒）: '))
runningData.append(input('跑步里程（米）: '))
runningData.append(input('步数: '))
codedData['time'] = ''.join(list(map(encode, runningData[0])))
codedData['distance'] = ''.join(list(map(encode, runningData[1])))
codedData['stepNum'] = ''.join(list(map(encode, runningData[2])))
print('\nEncoding...\n' + 'pwd_table: ' + "'pqwertyuio'" + ' timecode: ' + "'" + codedData[
    'time'] + "'" + ' distancecode: ' + "'" + codedData[
          'distance'] + "'" + ' stepnumcode: ' + "'" + codedData['stepNum'] + "'" + ' valid: ' + "'1'")

requestDatas = imei2json(imei)
token = GetToken(url, requestDatas, auth)
if token != 'failed':
    RunId = StartRunning(token, field)
    if RunId != 'failed':
        StopRunning(token, RunId, codedData['time'], codedData['distance'],
                    codedData['stepNum'], auth)
    else:
        print('获取RunId失败')
else:
    print('获取token失败')
