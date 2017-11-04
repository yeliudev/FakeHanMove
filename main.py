#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests

url = 'http://client1.aipao.me/api/token/QM_Users/Login'


def GetToken(url, datas=None):
    headers = {'Host': 'client1.aipao.me', 'Connection': 'keep-alive', 'Accept': '*/*', 'Version': 'B2.612',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'auth': 'B1B1135C4581F4A5C867698C60D72DAAE'}
    response = requests.get(url, params=datas, headers=headers)
    json = response.json()
    print(response.request.headers)
    print(response.headers)
    print(json)
    return json['Data']['Token']


def IMEI2JSON(IMEI):
    return {'IMEICode': IMEI}


def StartRunning(Token):
    headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.0.3; Scale/3.00)', 'Accept-Language': 'zh-Hans-CN;q=1',
               'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
    datas = {'Lat': '30.542006', 'Lng': '114.367925', 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
             'Level_Length': '2000', 'IsSchool': '1'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/startRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print('RunId' + json['Data']['RunId'])
    return json['Data']['RunId']


def StopRunning(Token, RunId):
    headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
               'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0', 'Accept-Language': 'zh-cn',
               'auth': 'B8ADC6D198B742591154471EE8B47AF70', 'Connection': 'keep-alive'}
    datas = {'S1': RunId, 'S2': 'wyyy', 'S3': 'gddx', 'S4': 'dro', 'S5': 'oyyy', 'S6': None, 'S7': '1',
             'S8': 'ygolnwprxd', 'S9': 'pyr'}
    requestURL = 'http://client1.aipao.me/api/' + Token + '/QM_Runs/EndRunForSchool'
    response = requests.get(requestURL, params=datas, headers=headers)
    json = response.json()
    print(json)
    return json


# IMEI = input('Please input your IMEI code:')
IMEI = 'c06a0681feb54b3d899e3869ed22be2c'
requestDatas = IMEI2JSON(IMEI)
Token = GetToken(url, requestDatas)
RunId = StartRunning(Token)
StopRunning(Token, RunId)
