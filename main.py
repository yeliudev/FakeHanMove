# Copyright (c) Ye Liu. All rights reserved.

import datetime
import hashlib
import random
import time

import requests

API_ROOT = 'http://client3.aipao.me/api/'


class HanMoveCracker(object):

    def __init__(self, uuid, imei, fieldCode, distance, runningTime, stepNum):
        self.uuid = uuid
        self.imei = imei
        self.distance = distance
        self.runningTime = runningTime
        self.stepNum = stepNum
        self.doRefresh = not distance

        self.header = {
            'Auth': None,
            'nonce': None,
            'timespan': None,
            'sign': None,
            'version': '2.11',
            'Accept': None,
            'User-Agent': None,
            'Accept-Encoding': None,
            'Connection': 'Keep-Alive'
        }

        if fieldCode == '1':
            self.location = ['30.544342', '114.366888']  # 桂园田径场
        if fieldCode == '2':
            self.location = ['30.545102', '114.372494']  # 九一二操场
        if fieldCode == '3':
            self.location = ['30.549832', '114.374182']  # 工学部体育场
        if fieldCode == '4':
            self.location = ['30.534084', '114.367382']  # 信息学部竹园田径场
        else:
            self.location = ['30.561585', '114.359509']  # 医学部杏林田径场

    def md5(self, s):
        return hashlib.md5(s.encode()).hexdigest()

    def enc(self, x):
        dict = {
            '0': 'p',
            '1': 'q',
            '2': 'w',
            '3': 'e',
            '4': 'r',
            '5': 't',
            '6': 'y',
            '7': 'u',
            '8': 'i',
            '9': 'o'
        }
        return dict[x]

    def wait(self, hour, minute, second):
        delta = datetime.datetime.replace(
            datetime.datetime.now(), hour=hour, minute=minute,
            second=second) - datetime.datetime.now()
        if delta.total_seconds() > 0:
            time_run = datetime.datetime.replace(
                datetime.datetime.now(),
                hour=hour,
                minute=minute,
                second=second)
        else:
            time_run = datetime.datetime.replace(
                datetime.datetime.now() + datetime.timedelta(days=1),
                hour=hour,
                minute=minute,
                second=second)
        print('')
        while True:
            delta = time_run - datetime.datetime.now()
            if delta.total_seconds() > 0:
                print(
                    '\rWaiting for next running...' +
                    str(int(delta.total_seconds())) + 's left',
                    end='')
            else:
                print('')
                break
            time.sleep(1)

    def get_token(self):
        print('\nTry getting token...Status: ', end='')
        url = API_ROOT + 'token/QM_Users/LoginSchool'

        res = requests.get(
            url, params={
                'IMEICode': self.imei
            }, headers=self.header).json()
        print('Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.token = res['Data']['Token']
            print('Token: %s' % res['Data']['Token'])
        else:
            exit('\nError: Token not found')

    def get_user_info(self):
        print('\nTry getting user information...Status: ', end='')
        url = API_ROOT + self.token + '/QM_Users/GS'

        res = requests.get(url, headers=self.header).json()
        print('Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.userId = str(res['Data']['User']['UserID'])
            self.nickname = res['Data']['User']['NickName']

            if not self.distance:
                self.distance = '2000' if res['Data']['User'][
                    'Sex'] == '男' else '1600'

            print(
                '\nHello, %s  UserID: %s  Sex: %s  distance: %s  runningTime: %ss  stepNum: %s'  # noqa
                % (self.nickname, self.userId,
                   ('male' if self.distance == '2000' else 'female'),
                   self.distance, self.runningTime, self.stepNum))
        else:
            exit('\nError: User information not found')

    def sign_data(self):
        print('\nTry signing data...Status: ', end='')
        try:
            self.header['timespan'] = str(time.time()).replace('.', '')[:13]
            self.header['nonce'] = str(random.randint(100000, 10000000))
            self.header['auth'] = 'B' + self.md5(self.md5(
                self.imei)) + ':;' + self.token
            self.header['sign'] = self.md5(self.token + self.header['nonce'] +
                                           self.header['timespan'] +
                                           self.userId).upper()

            print('Success')
            print('Auth: %s' % self.header['auth'])
            print('Sign: %s' % self.header['sign'])
        except Exception:
            print('Failed')
            exit('\nError: Sign error')

    def refresh_data(self):
        self.runningTime = str(random.randint(540, 1020))
        self.stepNum = str(random.randint(1400, 3500))

    def encode_data(self):
        print('\nTry encoding data...Status: ', end='')
        try:
            self.scoreCode = ''.join(
                map(self.enc, '5000' if self.distance == '2000' else '4000'))
            self.distanceCode = ''.join(map(self.enc, self.distance))
            self.runningTimeCode = ''.join(map(self.enc, self.runningTime))
            self.stepNumCode = ''.join(map(self.enc, self.stepNum))
            print('Success')
            print(
                '\n------------------------- Encoded data -------------------------'  # noqa
            )
            print('\n%-25s %-25s\n%-25s %-25s\n%-25s %-25s' %
                  ("pwd_table: 'pqwertyuio'", "scoreCode: '%s'" %
                   (self.scoreCode), "distanceCode: '%s'" %
                   (self.distanceCode), "runningTimeCode: '%s'" %
                   (self.runningTimeCode), "stepNumCode: '%s'" %
                   (self.stepNumCode), "location: %s" % (str(self.location))))
            print(
                '\n----------------------------------------------------------------'  # noqa
            )
        except Exception:
            print('Failed')
            exit('\nError: Encode data error')

    def start_running(self):
        print('\nTry getting RunId...Status: ', end='')
        url = API_ROOT + self.token + '/QM_Runs/SRS'
        data = {
            'S1': self.location[0],
            'S2': self.location[1],
            'S3': self.distance
        }

        res = requests.get(url, params=data, headers=self.header).json()
        print('Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.RunId = res['Data']['RunId']
            print('RunId: %s\n' % res['Data']['RunId'])
        else:
            exit('\nError: Start running error')

    def stop_running(self):
        print('\nTry uploading data...Status: ', end='')
        url = API_ROOT + self.token + '/QM_Runs/ES'
        data = {
            'S1': self.RunId,
            'S2': self.scoreCode,
            'S3': self.distanceCode,
            'S4': self.runningTimeCode,
            'S5': self.distanceCode,
            'S6': '',
            'S7': '1',
            'S8': 'pqwertyuio',
            'S9': self.stepNumCode
        }

        res = requests.get(url, params=data, headers=self.header).json()
        print('Success' if res['Success'] else 'Failed')

        if res['Success']:
            print('\n跑步数据成功上传，请登录阳光体育服务平台查询结果')
        else:
            print('\n跑步数据上传失败，请重试')
            exit('\nError: End running error')


def test_main():
    hmc = HanMoveCracker('uuid', None, None, None, None, None)
    assert hmc.uuid == 'uuid'


if __name__ == '__main__':
    print('\n---------------- Han Move Cracker by c1aris ----------------\n')

    uuid = input('UUID: ')
    imei = input('IMEI Code: ')

    fieldCode = input(
        '\n选择场地（1.桂园田径场 2.九一二操场 3.工学部体育场 4.信息学部竹园田径场 5.医学部杏林田径场）: ')

    if input('是否自动生成跑步参数（1.是 2.否）: ') == '1':
        distance = None
        runningTime = None
        stepNum = None
    else:
        distance = input('跑步里程（单位: 米 男2000 女1600）: ')
        runningTime = input('跑步时间（单位: 秒 0～1200）')
        stepNum = input('步数: ')

    uploadNow = input('是否立即开始上传数据（1.是 2.否）: ') == '1'

    hmc = HanMoveCracker(uuid, imei, fieldCode, distance, runningTime, stepNum)

    while True:
        if uploadNow:
            uploadNow = False
        else:
            hmc.wait(7, random.randint(0, 15), random.randint(0, 59))

        hmc.get_token()
        hmc.get_user_info()

        if hmc.doRefresh:
            hmc.refresh_data()

        hmc.encode_data()
        hmc.sign_data()
        hmc.start_running()

        extraTime = random.randint(1, 3)
        for i in range(int(hmc.runningTime) + extraTime):
            print(
                '\rWaiting for end of running...' +
                str(int(hmc.runningTime) + extraTime - i) + 's left',
                end='')
            time.sleep(1)

        hmc.stop_running()
