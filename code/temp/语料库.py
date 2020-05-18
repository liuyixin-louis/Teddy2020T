import requests
from bs4 import BeautifulSoup as bs
import re
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.rcParams["font.sans-serif"]=["SimHei"]
mpl.rcParams["axes.unicode_minus"]=False
from selenium import webdriver
from  time import sleep
import pandas as pd
import json
from  random import random
import re
from lxml import etree
from gne import GeneralNewsExtractor
token = '63ce8433d23e1f4d8cbd8bf14390fcc7'


# from newspaper import Article
# url = 'http://news.ifeng.com/a/20180504/58107235_0.shtml'
# news = Article(url, language='zh')
# news .download()
# news .parse()
# print(news.text)
# print(news.title)
# print(news.authors)


# from requests_html import HTMLSession
# session = HTMLSession()
# 平台：搜狗微信
driver = webdriver.Chrome()
driver.get('https://weixin.sogou.com/weixin')
driver.implicitly_wait(20) # 操作、获取元素时的隐式等待时间
driver.set_page_load_timeout(20) # 页面加载超时等待时间
sleep(20)
keyword = '确诊逗留'
page = '1'
url_ = 'https://weixin.sogou.com/weixin?query='+keyword+'&_sug_type_=&sut=3643&lkt=3%2C1588334155156%2C1588334155156&s_from=input&_sug_=y&type=2&sst0=1588334155259&page='+page+'&ie=utf8&w=01019900&dr=1'
# r = session.get(url_, verify=False)
# r.html.render()
# print (r.html.html)
# r = requests.get(url_)
# soup = bs(r.text,'html.parser')
# url_ = 'http://unclechen.github.io/2016/12/11/python%E5%88%A9%E7%94%A8beautifulsoup+selenium%E8%87%AA%E5%8A%A8%E7%BF%BB%E9%A1%B5%E6%8A%93%E5%8F%96%E7%BD%91%E9%A1%B5%E5%86%85%E5%AE%B9/'
for i in range(100):
    index = str(i+1)
    url_ = 'https://weixin.sogou.com/weixin?query='+keyword+'&_sug_type_=&sut=3643&lkt=3%2C1588334155156%2C1588334155156&s_from=input&_sug_=y&type=2&sst0=1588334155259&page='+index+'&ie=utf8&w=01019900&dr=1'
    driver.get(url=url_)
    sleep(0.5)
    html = driver.page_source
    soup  = bs(html,'"html.parser"')
    print (soup)
# session = HTMLSession()
# r = session.get(url_)
#
# result  = r.html.render()
# print (result)

# from requests_html import HTMLSession
# session = HTMLSession()
#
# r = session.get('https://www.cnblogs.com/yoyoketang/')
# r.html.render()  # 首次使用，自动下载chromium
# print (r.html.html)

# from requests_html import HTMLSession
# session = HTMLSession()
#
# r = session.get('https://www.cnblogs.com/yoyoketang/', verify=False)
# r.html.render()  # 首次使用，自动下载chromium
# # print(r.html.html)
# d = r.html.find("#profile_block", first=True)
# print(d.text)