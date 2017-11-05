#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

url = 'http://client1.aipao.me/api/token/QM_Users/Login'


def GetToken(url, datas=None):
    headers = {'Host': 'client1.aipao.me', 'Connection': 'keep-alive', 'Accept': '*/*', 'Version': 'B2.612',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'auth': 'B0614F0DFE3D91AA7DF9E68319001C498'}
    response = requests.get(url, params=datas, headers=headers)
    json = response.json()
    print('\nTry getting token...Success: ' + str(json['Success']))
    if json['Success']:
        print('Token: ' + json['Data']['Token'])
        return json['Data']['Token']
    else:
        return None


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


def StartRunning(Token):
    headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
    datas = {'Lat': '30.542006', 'Lng': '114.367925', 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
             'Level_Length': '2000', 'IsSchool': '1'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/startRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print('\nTry getting RunId...Success: ' + str(json['Success']))
    if json['Success']:
        print('RunId: ' + json['Data']['RunId'])
        return json['Data']['RunId']
    else:
        return None


def StopRunning(Token, RunId, timecode, distancecode):
    headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0', 'Accept-Language': 'zh-cn',
               'auth': 'B8ADC6D198B742591154471EE8B47AF70', 'Connection': 'keep-alive'}
    datas = {'S1': RunId, 'S2': 'tppp', 'S3': 'qooy', 'S4': timecode, 'S5': distancecode, 'S6': '', 'S7': '1',
             'S8': 'pqwertyuio', 'S9': 'qoiy'}
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
runningData = []
codedData = {'time': '900', 'distance': '2000'}
runningData.append(input('跑步时间（秒）: '))
runningData.append(input('跑步里程（米）: '))
codedData['time'] = ''.join(list(map(encode, runningData[0])))
codedData['distance'] = ''.join(list(map(encode, runningData[1])))
print('\nEncoding...\n' + 'pwd_table: ' + "'pqwertyuio'" + ' timecode: ' + "'" + codedData[
    'time'] + "'" + ' distancecode: ' + "'" + codedData[
          'distance'] + "'" + ' valid: ' + "'1'")

requestDatas = imei2json(imei)
Token = GetToken(url, requestDatas)
RunId = StartRunning(Token)
StopRunning(Token, RunId, codedData['time'], codedData['distance'])
