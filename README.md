# FakeHanMove

[![License](https://img.shields.io/badge/license-MIT-red.svg?colorB=D5283A#)](LICENSE)
[![Language](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
![GitHub last commit](https://img.shields.io/github/last-commit/goolhanrry/FakeHanMove.svg)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/goolhanrry/FakeHanMove.svg?colorB=ff7e00#)](https://github.com/goolhanrry/FakeHanMove)

一个让你优雅地躺在床上跑完汉姆的小工具，感谢 [zyc199847](https://github.com/zyc199847) 的思路，随缘更新，欢迎添加我的微信：`aweawds` 交流讨论

本工具仅供学习交流，因使用本工具而造成的一切不良后果由使用者自行承担，与作者无关

## Keywords

### &emsp;auth
&emsp;&emsp;位于 `Login` 和 `EndRunForSchool` 数据请求头中的签名，其中 `Login` 请求中可省略，加密方式暂时未知，猜测为 `'B' + MD5值` ，与上次登录的 token 有关

### &emsp;IMEI Code
&emsp;&emsp;32位字符串，包含数字和小写字母，用于标记用户，经测试抓包后长期有效

### &emsp;token
&emsp;&emsp;用于用户登录的临时令牌，由客户端发起 `Login` 请求获取，猜测生命周期为 30min 以上

## 已经实现的功能

* 自行选择跑步区域（桂园田径场、九一二操场、工学部体育场、信息学部竹园田径场、医学部杏林田径场）
* 随机产生跑步时长（540～1020秒）
* 随机产生步数（1400～3500步）
* 强制等待跑步结束后再上传数据，即发起 `StartRunForSchool` 请求后等待 `runningTime + 1` 秒后发起 `EndRunForSchool` 请求

## 即将实现的功能

* 暂无

## 使用方法

 1. 手机端打开汉姆运动并登录，使用 Fiddler 或 Charles 等工具对此过程抓包，获取登录请求头中的 `auth` 字段及请求数据中的 `Token` 和 `IMEICode` 字段
 2. 运行本工具，按提示输入相应内容，即可上传跑步数据
 
 注意：数据上传函数返回 `True` 不代表数据有效，请自行登录阳光体育服务平台查询数据有效性
