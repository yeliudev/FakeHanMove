# FakeHanMove

[![License](https://img.shields.io/badge/license-MIT-red.svg?colorB=D5283A#)](LICENSE)
[![Language](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/)
![GitHub last commit](https://img.shields.io/github/last-commit/goolhanrry/FakeHanMove.svg)
[![GitHub repo size in bytes](https://img.shields.io/github/repo-size/goolhanrry/FakeHanMove.svg?colorB=ff7e00#)](https://github.com/goolhanrry/FakeHanMove)

一个让你优雅地躺在床上跑完汉姆的小工具，随缘更新，欢迎添加我的微信：`aweawds` 交流讨论

本工具仅供学习交流，作者不会对因使用本工具而造成的一切不良后果负责

## 已经实现的功能

* 自行选择跑步区域（桂园田径场、九一二操场、工学部体育场、信息学部竹园田径场、医学部杏林田径场）
* 随机产生跑步时长（540～1140秒）
* 随机产生步数（1400～3500步）
* 自行选择是否跳过跑步等待时间，即发起 `StartRunForSchool` 请求后是否立即发起 `EndRunForSchool` 请求

## 即将实现的功能

* 暂无

## 使用方法

 1. 手机端打开汉姆运动并登录，使用Fiddler或Charles等工具对此过程抓包，获取登录请求头中的auth字段及请求数据中的Token和IMEICode字段
 2. 运行本工具，按提示输入相应内容，即可上传跑步数据
