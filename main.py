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
    print(response.request.headers)
    print(response.headers)
    print(json)
    return json['Data']['Token']


def imei2json(imei):
    return {'IMEICode': imei}


def StartRunning(Token):
    headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
    datas = {'Lat': '30.542006', 'Lng': '114.367925', 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
             'Level_Length': '2000', 'IsSchool': '1'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/startRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print('RunId: ' + json['Data']['RunId'])
    return json['Data']['RunId']


def StopRunning(Token, RunId):
    headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0', 'Accept-Language': 'zh-cn',
               'auth': 'B8ADC6D198B742591154471EE8B47AF70', 'Connection': 'keep-alive'}
    datas = {'S1': RunId, 'S2': 'tppp', 'S3': 'qooy', 'S4': 'otr', 'S5': 'wppp', 'S6': '', 'S7': '1',
             'S8': 'pqwertyuio', 'S9': 'pyr'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/EndRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print(json)
    return json


imei = input('Please input your IMEI code:')
if imei == 'default':
    imei = '766032a7ce6f4df2abc499bb2b79ecd0'
requestDatas = imei2json(imei)
Token = GetToken(url, requestDatas)
RunId = StartRunning(Token)
StopRunning(Token, RunId)
