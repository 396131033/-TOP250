#-*-  coding = utf-8 -*-  
#@Time : 2020/8/12 11:11
#@Author : 贾先圆
#@File: testBs4.py
#@Software: PyCharm
'''
    Beautifulsoup 将复杂HTML 文档转换成一个复杂的树形结构，每个节点都是Python对象，所有对象可以
    归纳为4种

    -Tag  #标签及其内容
    -NavigableSoup
    -BeautifulSoup
    -Comment
'''

from bs4 import BeautifulSoup
# file = open("./test.html",'rb')
# html = file.read()
# file.colse()
with open("./test.html","rb")as f:
    html = f.read()
    # print(html)
bs = BeautifulSoup(html,"html.parser")
'''
print(bs.title)  #取出title的所有内容  <title……/title>
print(bs.a)    #取第一个 a 标签 的所有内容  <a……/a>
# print(bs.head)  #取出title的所有内容   <head……/head>

# 1. Tag  标签及其内容，拿到它所找到的第一个内容
print(type(bs.head))  #out: <class 'bs4.element.Tag'>
# ==========================================================
'''

'''
# 2 NavigableString  标签里的内容（字符串）  string
print(bs.title.string)
print(type(bs.title.string))   #out: <class 'bs4.element.NavigableString'>
'''

# 3 拿到一个标签里的所有属性  attrs
print(bs.a.attrs)
#  out： {'href': 'https://accounts.douban.com/passport/login?source=movie', 'class': ['nav-login'], 'rel': ['nofollow']}


# print