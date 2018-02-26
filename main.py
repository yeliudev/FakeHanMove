#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests


class HanMoveCracker(object):

    def __init__(self, auth, token, imei, time, distance, stepNum, fieldCode):
        self.auth = auth
        self.token = token
        self.imei = imei
        self.RunId = ''

        self.timeCode = ''.join(map(self.enc, time))
        self.distanceCode = ''.join(map(self.enc, distance))
        self.stepNumCode = ''.join(map(self.enc, stepNum))

        if fieldCode == '1':
            self.point = ['30.544342', '114.366888']  # 桂园田径场
        if fieldCode == '2':
            self.point = ['30.545102', '114.372494']  # 九一二操场
        if fieldCode == '3':
            self.point = ['30.549832', '114.374182']  # 工学部体育场
        if fieldCode == '4':
            self.point = ['30.534084', '114.367382']  # 信息学部竹园田径场
        if fieldCode == '5':
            self.point = ['30.561585', '114.359509']  # 医学部杏林田径场

        print('\nEncoding...\n' + 'pwd_table: ' + '\'pqwertyuio\'' + ' timeCode: \'' + self.timeCode +
              '\'' + ' distanceCode: \'' + self.distanceCode + '\'' + ' stepNumCode: \'' + self.stepNumCode +
              '\'' + ' valid: ' + '\'1\'')

    def enc(self, x):
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

    def GetToken(self):
        url = 'http://client1.aipao.me/api/token/QM_Users/Login'
        headers = {'Host': 'client1.aipao.me', 'Connection': 'keep-alive', 'Accept': '*/*', 'Version': 'B2.162',
                   'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.2.6; Scale/3.00)',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                   'Accept-Ecoding': 'gzip, deflate', 'auth': self.auth}
        data = {'IMEICode': self.imei}
        print('\nTry getting token...Status: ', end='')
        try:
            response = requests.get(url, params=data, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                print('Token: ' + json['Data']['token'])
                self.token = json['Data']['token']
                return True
            else:
                return False
        except:
            print('Connection lost')
            return False

    def StartRunning(self):
        url = 'http://client1.aipao.me/api/' + self.token + '/QM_Runs/startRunForSchool'
        headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
                   'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.2.6; Scale/3.00)',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                   'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
        datas = {'Lat': self.point[0], 'Lng': self.point[1], 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
                 'Level_Length': '2000', 'IsSchool': '1'}
        print('\nTry starting running...Status: ', end='')
        try:
            response = requests.get(url, params=datas, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                print('RunId: ' + json['Data']['RunId'])
                return json['Data']['RunId']
            else:
                return False
        except:
            print('Connection lost')
            return False

    def EndRunning(self):
        url = 'http://client1.aipao.me/api/' + self.token + '/QM_Runs/EndRunForSchool'
        headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
                   'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                   'auth': self.auth, 'Connection': 'keep-alive'}
        datas = {'S1': self.RunId, 'S2': 'tppp', 'S3': self.distanceCode, 'S4': self.timeCode,
                 'S5': self.distanceCode, 'S6': '', 'S7': '1', 'S8': 'pqwertyuio', 'S9': self.stepNumCode}
        print('\nTry ending running...Status: ', end='')
        try:
            response = requests.get(url, params=datas, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            print(json)
            if json['Success']:
                print('\n跑步数据成功上传，请登录阳光体育服务平台查询结果')
                return True
            else:
                print('\n跑步数据上传失败，请重试')
                return False
        except:
            print('Connection lost')
            return False


auth = input('auth: ')
imei = input('IMEI code: ')
token = input('Token: ')
fieldCode = input('选择场地（1.桂园田径场 2.九一二操场 3.工学部体育场 4.信息学部竹园田径场 5.医学部杏林田径场）: ')
time = input('跑步时间（秒）: ')
distance = input('跑步里程（米）: ')
stepNum = input('步数: ')
if imei == '':
    imei = 'ba5b8f1229db4e8db9a3f299a94c93c2'

HMC = HanMoveCracker(auth, token, imei, time, distance, stepNum, fieldCode)
if HMC.token == '':
    if HMC.GetToken():
        if HMC.StartRunning():
            HMC.EndRunning()
else:
    if HMC.StartRunning():
        HMC.EndRunning()
