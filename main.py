#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import datetime
import time
import random
import hashlib


class HanMoveCracker(object):

    def __init__(self, uuid, imei, distance, runningTime, stepNum, fieldCode):
        self.uuid = uuid
        self.imei = imei
        self.UserID = 'unknown'
        self.nickname = 'unknown'
        self.power = 'unknown'
        self.distance = distance
        self.runningTime = int(runningTime) if runningTime else ''
        self.stepNum = int(stepNum) if stepNum else ''
        self.auth = ''
        self.token = ''
        self.RunId = ''
        self.distanceCode = ''
        self.runningTimeCode = ''
        self.stepNumCode = ''

        if fieldCode == '1':
            self.location = ['30.544342', '114.366888']  # 桂园田径场
        if fieldCode == '2':
            self.location = ['30.545102', '114.372494']  # 九一二操场
        if fieldCode == '3':
            self.location = ['30.549832', '114.374182']  # 工学部体育场
        if fieldCode == '4':
            self.location = ['30.534084', '114.367382']  # 信息学部竹园田径场
        if fieldCode == '5':
            self.location = ['30.561585', '114.359509']  # 医学部杏林田径场

    def RefreshData(self):
        self.runningTime = random.randint(540, 1020)
        self.stepNum = random.randint(1400, 3500)

    def EncodeData(self):
        print('\nEncoding data...')
        self.distanceCode = ''.join(map(self.enc, self.distance))
        self.runningTimeCode = ''.join(map(self.enc, str(self.runningTime)))
        self.stepNumCode = ''.join(map(self.enc, str(self.stepNum)))
        print('pwd_table: ' + '\'pqwertyuio\'' + ' runningTimeCode: \'' + self.runningTimeCode + '\'' +
              ' distanceCode: \'' + self.distanceCode + '\'' + ' stepNumCode: \'' + self.stepNumCode +
              '\'' + ' location: ' + str(self.location))

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

    def Wait(self, hour, minute, second):
        delta = datetime.datetime.replace(datetime.datetime.now(), hour=hour, minute=minute,
                                          second=second) - datetime.datetime.now()
        if delta.total_seconds() > 0:
            time_run = datetime.datetime.replace(datetime.datetime.now(), hour=hour, minute=minute, second=second)
        else:
            time_run = datetime.datetime.replace(datetime.datetime.now() + datetime.timedelta(days=1), hour=hour,
                                                 minute=minute, second=second)
        print('\n', end='')
        while True:
            delta = time_run - datetime.datetime.now()
            if delta.total_seconds() <= 0:
                print('\n', end='')
                break
            elif delta.total_seconds() > 1 and delta.total_seconds() <= 2:
                print('\rWaiting for next running...1 second left ')
            elif delta.total_seconds() <= 1:
                print('\rWaiting for next running...0 second left')
            else:
                print('\rWaiting for next running...' + str(int(delta.total_seconds())) + ' seconds left', end='    ')
            time.sleep(1)

    def GetToken(self):
        url = 'http://client1.aipao.me/api/token/QM_Users/Login'
        headers = {'Host': 'client1.aipao.me', 'Connection': 'keep-alive', 'Accept': '*/*', 'Version': 'B2.162',
                   'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.2.6; Scale/3.00)',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9', 'Accept-Ecoding': 'gzip, deflate'}
        data = {'IMEICode': self.imei}
        print('\nTry getting token...Status: ', end='')
        try:
            response = requests.get(url, params=data, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                print('Token: ' + json['Data']['Token'])
                self.token = json['Data']['Token']
                return True
            else:
                return False
        except:
            print('Connection lost')
            return False

    def CreateAuth(self):
        print('\nTry creating auth...Status: ', end='')
        try:
            hl = hashlib.md5()
            hl.update(self.uuid.encode(encoding='utf-8'))
            code = hl.hexdigest().upper() + ':' + self.token
            hl.update(code.encode(encoding='utf-8'))
            self.auth = 'B' + hl.hexdigest().upper()
            print('Success\nauth: ' + self.auth)
            return True
        except:
            print('Failed')
            return False

    def GetUsrInf(self, hasDistance=False):
        url = 'http://client1.aipao.me/api/' + self.token + '/QM_Users/GLIBU'
        headers = {'Host': 'client1.aipao.me', 'Accept': '*/*',
                   'User-Agent': 'HanMoves/2.16 (iPhone; iOS 11.2.6; Scale/3.00)',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                   'Accept-Ecoding': 'gzip, deflate', 'Connection': 'keep-alive'}
        print('\nTry getting user information...Status: ', end='')
        try:
            response = requests.get(url, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                self.UserID = str(json['Data']['User']['UserID'])
                self.nickname = json['Data']['User']['NickName']
                self.power = str(json['Data']['UserStatic']['Powers'])
                if not hasDistance:
                    self.distance = '2000' if json['Data']['User']['Sex'] == '1' else '1600'
                print('\nHello, ' + self.nickname + '  UserID: ' + self.UserID + '  sex: ' + (
                    'male' if self.distance == '2000' else 'female') + '  power: ' + self.power +
                      '  distance: ' + self.distance + 'm  runningTime: ' + str(self.runningTime) +
                      's  stepNum: ' + str(self.stepNum))
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
        datas = {'Lat': self.location[0], 'Lng': self.location[1], 'RunType': '1', 'RunMode': '1', 'FUserId': '0',
                 'Level_Length': '2000', 'IsSchool': '1'}
        print('\nTry getting RunId...Status: ', end='')
        try:
            response = requests.get(url, params=datas, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                print('RunId: ' + json['Data']['RunId'])
                self.RunId = json['Data']['RunId']
                return True
            else:
                return False
        except:
            print('Connection lost')
            return False

    def StopRunning(self):
        url = 'http://client1.aipao.me/api/' + self.token + '/QM_Runs/EndRunForSchool'
        headers = {'Host': 'client1.aipao.me', 'Accept-Ecoding': 'gzip, deflate', 'Accept': '*/*',
                   'User-Agent': 'HanMoves/2.16 CFNetwork/887 Darwin/17.0.0',
                   'Accept-Language': 'zh-Hans-CN;q=1, en-CN;q=0.9',
                   'auth': self.auth, 'Connection': 'keep-alive'}
        datas = {'S1': self.RunId, 'S2': 'tppp', 'S3': self.distanceCode, 'S4': self.runningTimeCode,
                 'S5': self.distanceCode, 'S6': '', 'S7': '1', 'S8': 'pqwertyuio', 'S9': self.stepNumCode}
        print('\nTry uploading data...Status: ', end='')
        try:
            response = requests.get(url, params=datas, headers=headers)
            json = response.json()
            print('Success' if json['Success'] else 'Failed')
            if json['Success']:
                print('\n跑步数据成功上传，请登录阳光体育服务平台查询结果')
                return True
            else:
                print(json)
                print('\n跑步数据上传失败，请重试')
                return False
        except:
            print('Connection lost')
            return False


doRefresh = True
distance = ''
runningTime = ''
stepNum = ''

uuid = input('UUID: ')
imei = input('IMEI code: ')
fieldCode = input('选择场地（1.桂园田径场 2.九一二操场 3.工学部体育场 4.信息学部竹园田径场 5.医学部杏林田径场）: ')
if input('是否随机生成跑步参数（1.是 2.否）: ') == '2':
    doRefresh = False
    distance = input('跑步里程（单位: 米 男2000 女1600）: ')
    runningTime = input('跑步时间（单位: 秒 0～1200）')
    stepNum = input('步数: ')

HMC = HanMoveCracker(uuid, imei, distance, runningTime, stepNum, fieldCode)

if input('是否立即开始上传数据（1.是 2.否）: ') == '2':
    HMC.Wait(7, random.randint(0, 15), random.randint(0, 59))

while True:
    if doRefresh:
        HMC.RefreshData()

    if HMC.GetToken():
        HMC.CreateAuth()
        HMC.GetUsrInf(HMC.distance)
        HMC.EncodeData()

        if HMC.StartRunning():
            extraTime = random.randint(1, 3)
            print('\n', end='')
            for i in range(HMC.runningTime + extraTime):
                if HMC.runningTime + extraTime - i > 1:
                    print('\rWaiting for end of running...' + str(HMC.runningTime + extraTime - i) + ' seconds left   ',
                          end='')
                else:
                    print('\rWaiting for end of running...1 second left ')
                time.sleep(1)
            HMC.StopRunning()
        else:
            print('\n获取RunId失败，请重试')
            break
    else:
        print('\n获取token失败，请重试')
        break
    HMC.Wait(7, random.randint(0, 15), random.randint(0, 59))
