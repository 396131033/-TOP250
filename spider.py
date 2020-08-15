#-*-  coding = utf-8 -*-  
#@Time : 2020/8/11 14:59
#@Author : 贾先圆
#@File: spider.py
#@Software: PyCharm

from bs4 import BeautifulSoup

import re   #正则
import requests
import xlwt  #进行Excel操作
import sqlite3  #进行SQLite 数据库操作
import urllib.request

def main():

    # 1.爬取网页
    base_url = 'https://movie.douban.com/top250?start='
    # html = askURL(base_url)

    # 2. 逐一解析数据
    datalist = getData(base_url)

    # 3.保存数据
    '''save_path = "./豆瓣电影Top250.xls"
    save_Data(save_path,datalist)
    '''
    dbpath = "movie.db"
    saveData2DB(dbpath,datalist)
# ============================================================================

# 1 全局标量  ——影片详情链接的规则
# findLink = re.compile(r'^<a href="(.*?)">$')   错误的，#? 0次或1次，有可能有的没有链接
findLink = re.compile(r'<a href="(.*?)">')     #全局变量
# 2 影片图片
findImgSrc = re.compile(r'img .*src="(.*?)" .*/>',re.S)  #re.S  让换行符包含在字符中，防止链接图像太长，换行了。
# 3 影片片名
findTitle = re.compile(r'span class="title">(.*)</span')
# 4 影片评分
findRating = re.compile(r'span class="rating_num" property="v:average">(.*)</span>')
# 5 找到评价人数
findJudge = re.compile(r'span>(\d*)人评价</span>')
# 6 找到概况
findInq = re.compile(r'<span class="inq">(.*)</span>')
# 7 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>',re.S)   #这里 ？ 一定要注意不能省略了。
# ==============================================================================

def askURL(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    request = urllib.request.Request(url,headers=headers)

    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
        # print(html)
        with open('test.html','w',encoding='utf-8')as f:
            f.write(html)

    except urllib.error.URLError as e:
        print('出错了')
        if hasattr(e,"code"):
            print(e.code)    #打印错误返回码
        if hasattr(e,"reason"):
            print(e.reason)
    return html

def getData(base_url):

    datalist = []
    for i in range(0,10):  #调用获取页面信息的函数， 10次，一页25条
        url = base_url + str(i*25)
        html = askURL(url)  #保存获取到的源码
    #     逐一解析网页
        soup = BeautifulSoup(html,"html.parser")

        c = 0;
        for item in soup.find_all('div',class_ = "item"):      #，div下的class标签，查找符合要求的字符串，形成列表
            # print(item)    #测试查看电影 item 全部信息
            data = []   #保存一部电影的所有信息
            item = str(item)
            # ============打印一个信息，便于参考写规则==========
            # print(item)
            # break

            # 获取影片详情的链接
            link = re.findall(findLink,item)[0]    #用正则表达式来查找指定的字符串,[0]选择找到的第1个
            #### link = re.findall(findLink, item)    # 显示的是列表，上面一个提取了列表中的元素
            # c = c+1
            # print("="*30,c,"="*30)    #检验获取链接个数
            # print(link)
            data.append(link)

            img = re.findall(findImgSrc,item)[0]
            data.append((img))

            title = re.findall(findTitle,item)    #片名有的可能有中文和外文名
            if len(title)==2:
                chinese_title = title[0]
                data.append(chinese_title)      #添加中文名
                english_title = title[1].replace("/","")   #去掉无关的符号
                data.append(english_title)                 #添加外文名
            else:
                data.append(title[0])
                data.append(' ')      #如果没有外国名，外国名位置留空

            score = re.findall(findRating,item)[0]
            data.append(score)

            judgeNum = re.findall(findJudge,item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq,item)   #可能不存在，所以不能直接用[0]
            if len(inq) != 0 :
                inq = inq[0].replace("。","")  #去掉句号
                data.append(inq)
            else:
                data.append(" ")       #留空

            bd = re.findall(findBd,item)[0]
            bd = re.sub('<br(\s+)?/>(\s+)?'," ",bd)   #去掉（<br/>）
            bd = re.sub('/'," ",bd)        #替换 /
            bd = bd.strip()         #去掉前后空格
            data.append(bd)

            datalist.append(data)    #把处理好的一部电影信息放入datalist

    # =========验证爬取效果===========
    # for i in datalist:
    #     print(i)

    return datalist


def save_Data(save_path,datalist):
    # 保存到Excel中
    print("*"*20+"开始保存……"+"*"*20)
    workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
    worksheet = workbook.add_sheet("豆瓣评分Top250",cell_overwrite_ok=True)   #cell_overwrite_ok 内容覆盖
    # ===========创建列名============
    col = ['电影详情链接','图片链接','影片中文名','影片外文名','评分','评价人数','概况','相关信息']
    for i in range(0,8):
        worksheet.write(0,i,col[i])
    for i in range(0,250):
        print("====正在写入第{}条数据====".format(i+1))
        data = datalist[i]
        for j in range(0,8):
            worksheet.write(i+1,j,data[j])

    # workbook.save("doubantop250.xls")
    workbook.save(save_path)

def saveData2DB(dbpath,datalist):
    init_db(dbpath)   #创建数据库
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    # value(%s)  #%s 占位
    # data[index] = '"' + data[index] + '"'  # 全部转换为字符，尤其是链接
    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index==5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
            insert into movie250
            (
                info_link,pic_link,cname,ename,score,rated,instroduction,info
            ) 
            values(%s)'''%",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("数据插入完毕！")



    conn = sqlite3.connect(dbpath)

    print(".......")

def init_db(dbpath):
    sql = '''
        create table movie250
            (
                id integer primary key autoincrement,
                info_link text,
                pic_link text,
                cname varchar,
                ename varchar,
                score numeric,
                rated number,
                instroduction text,
                info text
            )
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
    # init_db("movietest.db")
    print('*'*20+"爬取完毕"+'*'*20)