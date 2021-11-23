# Copyright (c) StLeoX. All rights reserved.

import datetime
import hashlib
import random
import threading
import time

import requests
import csv

# changed client4->client3
API_ROOT = 'http://client3.aipao.me/api/'

finished = []


class HanMoveCracker(object):

    def __init__(self, uuid, imei, fieldCode, distance, runningTime, stepNum):
        self.uuid: str = uuid
        self.imei: str = imei
        self.distance: str = distance
        self.runningTime: str = runningTime
        self.stepNum: str = stepNum
        self.doRefresh = not distance
        self.task_name = None

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
        # 最珍贵的数据！
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

    # 验证token
    def get_token(self):
        # print('\nTry getting token...Status: ', end='')
        url = API_ROOT + 'token/QM_Users/LoginSchool'

        res = requests.get(
            url, params={
                'IMEICode': self.imei
            }, headers=self.header).json()
        print('get_token Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.token = res['Data']['Token']
            # print('Token: %s' % res['Data']['Token'])
        else:
            exit('\nError: Token not found')

    # 获取用户信息
    def get_user_info(self):
        # print('\nTry getting user information...Status: ', end='')
        url = API_ROOT + self.token + '/QM_Users/GS'

        res = requests.get(url, headers=self.header).json()
        print('get_user_info Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.userId = str(res['Data']['User']['UserID'])
            self.nickname = res['Data']['User']['NickName']

            if not self.distance:
                self.distance = '2000' if res['Data']['User'][
                                              'Sex'] == '男' else '1600'

        else:
            exit('\nError: User information not found')

    # mock data
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

            print('sign_data Success')

        except Exception:
            print('Failed')
            exit('\nError: Sign error')

    def refresh_data(self):
        self.runningTime = str(random.randint(600, 700))
        self.stepNum = str(random.randint(1400, 3500))

    def encode_data(self):
        # print('\nTry encoding data...Status: ', end='')
        try:
            self.scoreCode = ''.join(
                map(self.enc, '5000' if self.distance == '2000' else '4000'))
            self.distanceCode = ''.join(map(self.enc, self.distance))
            self.runningTimeCode = ''.join(map(self.enc, self.runningTime))
            self.stepNumCode = ''.join(map(self.enc, self.stepNum))
            print('encode_data Success')

        except Exception:
            print('Failed')
            exit('\nError: Encode data error')

    def start_running(self):
        # print('\nTry getting RunId...Status: ', end='')
        url = API_ROOT + self.token + '/QM_Runs/SRS'
        data = {
            'S1': self.location[0],
            'S2': self.location[1],
            'S3': self.distance
        }

        res = requests.get(url, params=data, headers=self.header).json()
        print('start_running Success' if res['Success'] else 'Failed')

        if res['Success']:
            self.RunId = res['Data']['RunId']
            print('RunId: %s\n' % res['Data']['RunId'])
        else:
            exit('\nError: Start running error')

    # 唯时间不可改！
    def stop_running(self):
        # print('\nTry uploading data...Status: ', end='')
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
        print('stop_running Success' if res['Success'] else 'Failed')
        finished.append(self.task_name)

        if int(self.runningTime) == max(times):  # 针对最后一个任务才能exit(0)
            if res['Success']:
                print("finished:")
                for i in finished:
                    print(i)
                print('\n全部跑步数据成功上传，请登录阳光体育服务平台查询结果。')

                exit(0)
            else:
                print('\n存在跑步数据上传失败。')
                raise Exception('\nError: End running error')


times = [0]  # 计时


def single_mock(uuid_, imei_, field_code_, task_name_):
    uploadNow = True
    hmc = HanMoveCracker(uuid_, imei_, field_code_, None, None, None)
    hmc.task_name = task_name_

    while True:
        if uploadNow:
            uploadNow = False
        else:
            hmc.wait(7, random.randint(0, 15), random.randint(0, 59))
        try:
            hmc.get_token()
            hmc.get_user_info()

            if hmc.doRefresh:
                hmc.refresh_data()

            hmc.encode_data()
            hmc.sign_data()
            hmc.start_running()

            # extraTime = random.randint(1, 3)
            # for i in range(int(hmc.runningTime) + extraTime):
            #     print(
            #         '\rWaiting for end of running...' +
            #         str(int(hmc.runningTime) + extraTime - i) + 's left',
            #         end='')
            #     time.sleep(1)
            times.append(int(hmc.runningTime))
            time.sleep(int(hmc.runningTime))
            print("\nstart to update time data")
            hmc.stop_running()
        except Exception as e:
            print(e)


if __name__ == '__main__':
    with open('./accounts.txt') as f:
        lines = csv.DictReader(f)
        tasks = {}
        for line in lines:
            if line['enable'] == '1':
                tasks[line['name']] = threading.Thread(target=single_mock,
                                                       args=(line['uuid'], line['imei'], 4, line['name']))
                print(f"{line['name']}'s task starting...")
                tasks[line['name']].start()
        time.sleep(3)
        print(f"===========\nAll tasks will finish after {max(times)} seconds.")
        # main thread sleep
        for i in range(max(times) + 10):
            if i % 10 == 0:
                print('\rWaiting for end of running...' + str(max(times) - i) + 's left', end='')
            time.sleep(1)
