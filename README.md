# FakeHanMove

[![License](https://img.shields.io/badge/license-MIT-red.svg?colorB=D5283A#)](LICENSE)
[![Language](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)

一个让你优雅地躺在床上跑完汉姆的小工具，感谢 [zyc199847](https://github.com/zyc199847) 和 [李叶](https://github.com/HackerLiye) 的思路

本工具仅供学习交流，因使用本工具而造成的一切不良后果由使用者自行承担，与作者无关

## Keywords

### &emsp;auth

&emsp;&emsp;33 位字符串，位于 `Login` 和 `EndRunForSchool` 数据请求头中的签名，其中 `Login`
请求中可省略，加密方式为 `'B' + MD5(MD5(UUID) + ':' + token) ` ，其中 `UUID` 可通过对首次微信登录抓包获取

### &emsp;IMEI Code

&emsp;&emsp;32 位字符串，包含数字和小写字母，用于标记用户，经测试首次微信登录授权后长期有效

### &emsp;token

&emsp;&emsp;32 位字符串，包含数字和小写字母，用于用户登录的临时令牌，由客户端发起 `Login` 请求获取，生命周期 3h 以上

## 已经实现的功能

* 获取用户信息，包括昵称、UserID、性别，并通过性别判定跑步里程
* 每天早上随机时间自动上传数据
* 自行选择跑步区域（桂园田径场、九一二操场、工学部体育场、信息学部竹园田径场、医学部杏林田径场）
* 随机产生跑步时长（540～1020秒）
* 随机产生步数（1400～3500步）
* 强制等待跑步结束后再上传数据，即发起 `StartRunForSchool` 请求后等待 `runningTime + (1～3)` 秒后发起 `EndRunForSchool` 请求

## 即将实现的功能

* 暂无

## 使用方法

1. 手机端打开汉姆运动，注销账号
2. 重新使用微信对汉姆运动授权，使用 Fiddler 或 Charles 等工具对此过程抓包，获取登录请求头中的 `IMEI` 字段和返回数据中的 `IMEICode` 字段
3. 配置 [Python3](https://www.python.org/) 运行环境
4. Terminal 或 CMD 执行 `pip install requests` 安装 requests 库
5. 运行 `main.py` ，按提示输入相关参数，即可上传跑步数据

注意：数据上传函数返回 `True` 不代表数据有效，请自行登录阳光体育服务平台查询数据有效性

## 软件截图

<p align="center">
  <img with="850" height="580" src=".github/screenshot.png" alt="screenshot">
</p>

## 更新说明

- 支持多用户批量进行，使用多线程实现。
- accounts.txt 中三个字段分别是：
    - name：用户名（随便写）
    - uuid：Token
    - imei：IMEICode  
      只需要将抓到的字段填进去就可以了，**不能改首行**。
- 另外有一个小小的温馨提示：   
  针对Android抓包，不要在手机上操作比如使用Package Capture App，这些App对Android11已经失效了。  
  建议使用Fiddler或者是Charles  
  [Fiddler抓包手机流量教程 ](https://www.cnblogs.com/WindrunnerMax/p/12558258.html)

