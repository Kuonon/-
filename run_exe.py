import os
import wmi
import sys
import uuid
import time
import socket
import requests
import configparser
from fake_user_agent import user_agent

BASE_DIR = os.path.dirname(os.path.realpath(sys.executable))
conf = configparser.ConfigParser()
curpath = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(curpath, BASE_DIR + '\config.ini')
conf.read(path, encoding="utf-8")
loginid_value = conf['login']['id'] #导入账号
password_value = conf['login']['password'] #导入密码
try_value = conf['failed']['try_times'] #导入失败尝试次数
try_interval = conf['failed']['try_interval'] #导入失败尝试时间间隔
connect_detect_interval = conf['failed']['connect_detect_interval'] #导入网络检测时间间隔

hostip = socket.gethostbyname(socket.gethostname()) #获取本机ip地址

a = 0
while a == 0:
    value = []
    wmi_obj = wmi.WMI()
    wmi_sql = "select IPAddress,DefaultIPGateway from Win32_NetworkAdapterConfiguration where IPEnabled=TRUE"
    wmi_out = wmi_obj.query(wmi_sql)
    for dev in wmi_out:
        try:
            value.append(dev.DefaultIPGateway[0])
        except:
            pass
    if len(value) != 0:
        if value[0] == '172.20.0.1':
            print('已连接YMUN网络，即将自动登录')
            a = 1
        else:
            print("非YMUN校园网络，即将重试")
            a = 0
            time.sleep(int(connect_detect_interval))
    else:
        print("请连接YMUN校园网络，即将重试")
        a = 0
        time.sleep(int(connect_detect_interval))

i = 0
while i != int(try_value) + 1:
    try:
        mac_raw = uuid.UUID(int=uuid.getnode()).hex[-12:]
        mac = ":".join([mac_raw[e:e + 2] for e in range(0, 11, 2)]).upper() #获取本机mac地址

        headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
                        'Connection': 'keep-alive',
                        'Content-Length': '346',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Cookie': '',
                        'Host': '172.16.6.6',
                        'Referer': 'http://172.16.6.6',
                        'Origin': 'http://172.16.6.6',
                        'Sec-Fetch-Dest': 'empty',
                        'Sec-Fetch-Mode': 'cors',
                        'Sec-Fetch-Site': 'same-site',
                        'User-Agent': user_agent(),  # 模拟用户登录设备
                    } #设置请求头

        data = {
                        'loginType': "",
                        'auth_type': "0",
                        'isBindMac1': "1",
                        'pageid': "22",
                        'templatetype': "1",
                        'listbindmac': "1",
                        'recordmac': "0",
                        'isRemind': "0",
                        'loginTimes': "",
                        'groupId': "",
                        'distoken': "",
                        'echostr': "",
                        'url': "http://1.1.1.1",
                        'isautoauth': "",
                        'notice_pic_loop2': "/portal/uploads/pc/demo2/images/bj.png",
                        'notice_pic_loop1': "/portal/uploads/pc/demo2/images/logo.png",
                        'userId': loginid_value,
                        'passwd': password_value
                    } #设置传递参数

        url = 'http://172.16.6.6/webauth.do?wlanacip=1.1.1.1&wlanacname=ZAX-BAS&wlanuserip=' + str(hostip) + '&mac=' + str(mac) + '&vlan=0&url=http://1.1.1.1' #组合请求ip地址

        response_raw = requests.post(url, headers=headers, data=data) #提交请求

        time.sleep(1)
        url_2 = "http://www.baidu.com"
        response = requests.get(url_2)
        value = 1
    except:
        value = 0

    if value == 1:
                i = int(try_value) + 1
                print("自动登录成功")
    else:
            i = i + 1
            print("自动登录失败，即将重新尝试")
            time.sleep(int(try_interval))
