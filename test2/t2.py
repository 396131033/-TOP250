#-*-  coding = utf-8 -*-  
#@Time : 2020/8/11 14:56
#@Author : 贾先圆
#@File: t2.py
#@Software: PyCharm

'''
# 导入test1（包） 文件 中的 函数
# 引入自定义模块
from test1 import t1

# 引入系统模块
import sys
import os

sum = t1.addfun(3,5)
print(sum)
'''

'''
import urllib.parse
import urllib.request
data = bytes(urllib.parse.urlencode({"hello":"world"}),encoding='utf-8')
response = urllib.request.urlopen("http://httpbin.org/post",data=data)
print(response.read().decode('utf-8'))
'''

import requests   #requests 不需要转译parse，会自动转译   注意这里是 发送post 请求而不是get请求
try:

    response = requests.post("http://httpbin.org/post",timeout = 0.01)
    response = requests.post("http://httpbin.org/post",data={"hello":"world"})
    print(response.text)
except Exception as result:
    print('超时了！')
