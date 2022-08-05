import xlrd
import xlwt
import xlsxwriter
import requests
import re
import json
import urllib.request
from lxml import etree
from bs4 import BeautifulSoup
from openpyxl import workbook  # 写入Excel表所用
import time


# 获取总共有多少页
def get_page(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req).read()
    response = json.loads(response.decode("utf-8"))
    # response = urllib.request.urlopen(url).read()
    # response = json.loads(response.decode("utf-8").encode('GBK'))
    total = response['data']['total']

    page = int(total / 12) + 1
    print("page:", page)
    return page


# 循环爬取页数
def get_list(page):
    for i in range(0, page):
        url = 'http://www.mafengwo.cn/together/travel/more?' + flag + '&' + 'offset=' + str(
            i) + '&' + mddid
        get_matehtml(url)
        time.sleep(8)
        print("#" * 20)
        print("i,url:", i, url)


# 获取链接网址
def get_matehtml(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=url, headers=headers)
    response = urllib.request.urlopen(req).read()
    response = json.loads(response.decode("utf-8"))
    # response = json.loads(urllib.request.urlopen(url).read().decode("utf-8").encode('GBK'))
    html = response['data']['html']
    pat1 = 'a href=\"(.*?)" target=\"_blank\">'
    rst1 = re.compile(pat1).findall(html)
    i = 1
    for html in rst1:
        print("get_matehtml:", 'http://www.mafengwo.cn' + html)
        get_detail('http://www.mafengwo.cn' + html)



# 获取每个结伴明细信息
def get_detail(html):
    global togetherlist
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib.request.Request(url=html, headers=headers)
    response = urllib.request.urlopen(req).read().decode("utf-8")
    print(response)


    # response = urllib.request.urlopen(html).read().decode("utf-8")
    # 获取标题
    pat1 = '<title>(.*?)</title>'
    title = re.compile('<title>(.*?)</title>').findall(response)[0]
    print("title:", title)
    see = re.compile('<span>(.*?)</span>人').findall(response)[0]
    sign = re.compile('<span>(.*?)</span>人').findall(response)[1]
    follow = re.compile('<span>(.*?)</span>人').findall(response)[2]
    soup = BeautifulSoup(urllib.request.urlopen(req).read(), 'lxml')
    title = soup.title.get_text()
    gooff = re.compile('出发时间：(.*?)</span>').findall(response)[0]
    days = re.compile('大约：(.*?)</span>').findall(response)[0]
    des = re.compile('目的地：(.*?)</span>').findall(response)[0]
    fro = re.compile('出发地：(.*?)</span>').findall(response)[0]
    num = re.compile('希望人数：(.*?)</span>').findall(response)[0]
    enrollment = re.compile('<span><em>(.*?)</em>').findall(response)[0]
    female = re.compile('<span>MM(.*?) <i').findall(response)[0]
    male = re.compile('<span>GG(.*?) <i').findall(response)[0]
    description_tmp = soup.select('div[class="desc _j_description"]')[0]
    description = description_tmp.get_text()

    joinlist_tmp = soup.select('.mod-joinlist div ul li .name')
    attention_tmp = soup.select('.mod-attentionUser div ul li a')
    comment_tmp = soup.select('.mod-comment ul div .comm_con')
    # 获取报名的列表
    joinlist = get_joinlist(joinlist_tmp)
    # 获取关注的列表
    attentionlist = get_attentionlist(attention_tmp)
    # 获取评论列表
    commentlist = get_commentlist(comment_tmp)
    togetherlist.append(
        [html, title, see, sign, follow, gooff, days, des, fro, num, enrollment, female, male, description, joinlist,
         attentionlist, commentlist])


# 获取报名结伴列表整理
def get_joinlist(html):
    joinlist = []
    for tmp in html:
        tmp1 = tmp.attrs['href']
        tmp2 = tmp.get_text()
        tmp3 = [tmp1, tmp2]
        joinlist.append(tmp1)
    return '-'.join(joinlist)


# 获取关注结伴列表整理
def get_attentionlist(html):
    # print ("html:",html)
    attentionlist = []
    for tmp in html:
        attentionlist.append(tmp.attrs['href'])
    return '-'.join(attentionlist)


# 获取评论列表
def get_commentlist(html):
    # print ("html:",html)
    commentlist = []
    for tmp in html:
        # print ("tmp:",tmp.select('.comm_info span'))
        comm_id = tmp.select('.comm_info a')[0].attrs['href']
        comm_name = tmp.select('.comm_info a')[0].get_text()
        comm_grade = tmp.select('.comm_info a')[1].get_text()
        comm_time = tmp.select('.comm_info span')[0].get_text()
        comm_word = tmp.select('.comm_word')[0].get_text()
        # print ("tmp_comment:",comm_id,comm_name,comm_grade,comm_time,comm_word)
        commentlist.append(comm_word)
    return '@@'.join(commentlist)


# 把爬虫结果写入到excel中
def data_write(file_path, datas):
    print("begin to write:", len(datas))

    workbook = xlsxwriter.Workbook('D:\\Mafengwo\\jieban\\test03.xlsx')  # 生成表格
    worksheet = workbook.add_worksheet(u'sheet1')  # 在文件中创建一个名为TEST的sheet,不加名字默认为sheet1
    # 将数据写入第 i 行，第 j 列
    i = 0
    for data in datas:
        for j in range(len(data)):
            # print ("i,j,data[j]:",i,j,type(data[j]),data[j])
            worksheet.write(i, j, data[j])
        i = i + 1

    workbook.close()


# 爬取马蜂窝结伴信息入口：
if __name__ == '__main__':
    flag = 'flag=3'
    offset = 'offset=0'
    mddid = 'mddid=10442'
    timelag = '3'

    # base_url = 'http://www.mafengwo.cn/together/travel/more?' + flag + '&' + offset + '&' + mddid + '&' + 'timeFlag=3&timestart='
    base_url = 'http://www.mafengwo.cn/together/travel/more?' + flag + '&' + offset + '&' + mddid
    print("base_url:", base_url)

    page = get_page(base_url)
    # data3 = urllib.request.urlopen(url).read()
    # data3 = data3.decode("utf-8").encode('GBK')
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    # req = urllib.request.Request(url=url, headers=headers)
    # data3 = urllib.request.urlopen(req).read()
    # data3 = json.loads(response.decode("utf-8"))

    global togetherlist
    togetherlist = []
    get_list(10)
    print("len(togetherlist):", len(togetherlist))

    # 创建Excel表并写入数据
    data_write("D:\\Mafengwo\\jieban\\test1.xlsx", togetherlist)


