#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:SunXiuWen
# make_time:2018/12/14
from YDMHTTPDemo3 import YDMHttp
import requests
from lxml import etree
import json
import time
import re

def get_code(code_img):
    """调用云打码平台识别验证码
    本代码为平台提供
    """
    # 平台普通用户名
    username = 'xxx'

    # 密码
    password = 'xxx'

    # 软件ＩＤ，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appid = 6003

    # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
    appkey = 'xxx'

    # 图片文件
    filename = code_img

    # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
    codetype = 1004

    # 超时时间，秒
    timeout = 10

    # 检查
    if (username == 'username'):
        print('请设置好相关参数再测试')
    else:
        # 初始化
        yundama = YDMHttp(username, password, appid, appkey)

        # 登陆云打码
        uid = yundama.login()
        print('uid: %s' % uid)

        # 查询余额
        balance = yundama.balance()
        print('balance: %s' % balance)

        # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
        cid, result = yundama.decode(filename, codetype, timeout)
        print('cid: %s, result: %s' % (cid, result))

        return result


url = 'http://crm.pythonav.com/rbac/check_code/????????????'

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Mobile Safari/537.36'
}

code = requests.get(url=url, headers=headers).content

with open('./code.png', 'wb') as f:
    f.write(code)

code_text = get_code('./code.png')
print(code_text)