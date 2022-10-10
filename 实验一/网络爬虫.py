import time

import bs4
import requests
from bs4 import BeautifulSoup
import re
import os
import string
import random

def getHTMLText(url):
    try:
        kv = {'user-agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=kv)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "访问异常"

def parasePage(ulst,url,root):
    html=getHTMLText(url)
    soup = BeautifulSoup(html, 'html.parser')
    file_list=[]#存取整个网页解析信息
    #解析html，取出title
    if isinstance(soup.title, bs4.element.Tag):
        title_file='Title:'+soup.title.text
        file_list.append(title_file)
    else:
        title_file='Title:'+'无标题'
        file_list.append(title_file)
    #添加当前页链接到文档
    url_file='Url  :'+url
    file_list.append(url_file)

    # 解析html，取出context
    context_file = "Context如下\n"
    file_list.append(context_file)

    span_context=soup.find_all('span')
    for sc in span_context:
        if isinstance(sc,bs4.element.Tag):
            file_list.append(sc.text.strip())#

    all_context = soup.find_all('p')
    for con in all_context:
        if isinstance(con, bs4.element.Tag):  # 过滤非标签
            con_file=con.text.strip()
            file_list.append(con_file.strip())#.center(100," ")

    root_path = root#保留，方便更改
    fpath = getPath(url, root_path)
    writetoFile(file_list, fpath, root_path)
    file_list.clear()

    #解析html，取出url
    all_url = soup.find_all('a')
    for ul in all_url:
        try:
            href=ul.attrs['href']
            ulst.append(re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', href)[0])
        except:
            continue
    print('=====网页  '+url+'  爬取完成=====')


def writetoFile(lst,fpath,root):
    try:
        if not os.path.exists(root):
            os.mkdir(root)             #如果没有则建立文件夹路径
        if not os.path.exists(fpath):
            lst_content=""
            for l in lst:
                lst_content=lst_content+l+'\n' #将列表中的内容转为字符串
            if len(lst_content)!=0:
                with open(fpath, 'a',encoding="utf-8")as f:
                    f.write(lst_content)
                    f.close()
                    print('文件保存成功')
            else:
                print('爬取数据为空')
        else:
            print('文件已经存在')
    except:
        print('写入失败')

def getPath(url,root):
    if len(url.split('/')[-1])==0:
        # file_name=''.join(random.sample(string.ascii_letters + string.digits, 16))
        file_name=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    else:
        file_name=url.split('/')[-1][len(url.split('/')[-1])//2:]
    path = root + file_name+".txt"
    return re.sub(r'\?| |%|&|_|=|-','',path)

def autoCrawl(url_lst,root,depth):
    temp_list=[]
    if len(url_lst)<depth:
        for i in range(0, len(url_lst)):
            parasePage(temp_list, url_lst[i], root)
            temp_list.clear()
            time.sleep(10)
    else:
        # first_url=random.randint(0,len(url_lst)-depth)
        first_url=0
        for i in range(first_url,first_url+depth):
            parasePage(temp_list,url_lst[i],root)
            temp_list.clear()
            time.sleep(10)

def startParase(root,keyword,website_list,depth):
    # 分别从三个网站进行关键词搜索
    for website in website_list:
        url_list = []
        root_file=root+website.split('/')[-2]+"//"
        url=website+keyword
        parasePage(url_list,url,root_file)
        autoCrawl(url_list,root_file,depth)

def main():
    root = "E://Python/自然语言处理/实验一/语料库/"
    keyword=input("请输入需要查取的内容：")
    website_list=["https://www.cdsb.com/Home/Index/search?title=","http://s.99zuowen.com/cse/search?s=16033497922828948127&q=","https://www.so.com/s?q=","https://sou.chinanews.com.cn/search.do?q="]
    while True:
        try:
            depth=int(input("请输入自动搜索链接数："))
        except:
            print("输入有误，请重新输入")
        else:
            break
    startParase(root,keyword,website_list,depth)

main()