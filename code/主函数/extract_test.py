# packet

import requests
from bs4 import BeautifulSoup
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

driver = webdriver.Chrome()
driver.get('https://weibo.com')

driver.implicitly_wait(20) # 操作、获取元素时的隐式等待时间
driver.set_page_load_timeout(20) # 页面加载超时等待时间



def get_content(url, driver):
    '''
        input:url,driver
        output:sname,text,images
    '''

    content = ''
    sname = ''
    images = []

    templates = ['weibo.com', 'mp.weixin.qq.com', 'm.weibo.cn', 'm.mp.oeeee.com']
    # 判断是否在模板库中
    in_ = False
    for t in templates:
        if t in url:
            in_ = True
            break
    if in_:
        if 'mp.weixin.qq.com' in url:
            # 微信公众号
            print(url, 'wx')

            driver.get(url)
            sleep(0.5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            sn, sc = ['#js_name', '#js_content']
            resource_name = soup.select(sn)
            content_selector = soup.select(sc)[0]
            content = content_selector.get_text()
            resource_name = resource_name[0].get_text()
            sname = re.sub(r'[^\u4e00-\u9fa5]', '', resource_name)
            imglist = []
            imgs = content_selector.find_all('img')

            if len(imgs) >= 1:
                for img in imgs:
                    img_dict = img.attrs
                    if 'data-type' in img_dict:
                        if 'gif' in img_dict['data-type']:
                            continue
                        else:
                            if 'data-src' in img_dict:
                                images.append(img_dict['data-src'])
                            elif 'src' in img_dict:
                                images.append(img_dict['src'])

        elif 'm.weibo.cn' in url:
            # 微博手机端
            print(url, 'mwb')
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            r = soup.select(
                '#app > div.lite-page-wrap > div > div.main > div > div > header > div.m-box-dir.m-box-col.m-box-center > div > a > h3')
            sname = re.sub(r'[^\u4e00-\u9fa5]', '', r[0].text)
            c = soup.find_all(attrs={'class': 'weibo-text'})
            content = c[0].text

        elif 'weibo.com' in url:
            # 微博pc端
            print(url, 'pcwb')
            driver.get(url)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            c = soup.find_all(attrs={'class': 'WB_text'})
            content = c[0].text
            sname = c[0].attrs['nick-name']

        elif 'm.mp.oeeee.com' in url:
            # 南方都市报
            print(url, 'nd')
            #             url = 'https://m.mp.oeeee.com/a/BAAFRD000020200203257514.html?layer=4&share=chat&isndappinstalled=12'
            driver.get(url)
            sleep(0.5)
            html = driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            s = soup.find_all(attrs={'class': 'name avatar_click'})
            sname = s[0].text
            c = soup.find_all(attrs={'id': 'docContent'})
            content = c[0].text

    else:
        diffbot_invaild = False
        # 不在模板库里，调用diffbot的api进行视觉分割+机器学习的正文抽取
        # url = 'https://mp.weixin.qq.com/s/HTsNM1zxEAx3IqoF1uYnYA'
        api = 'https://api.diffbot.com/v3/article'
        params = {
            'token': token,
            'url': url,
            'fields': 'images'
        }
        response = requests.get(api, params=params)
        #         print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        result = response.json()
        if 'error' in result:
            print(url, 'gne')
            # 无法用api,iffbot失效，转用基于文本密度和符号密度的GNE工具包抽取正文
            print(response.text, url)
            driver.get(url)
            sleep(0.5)
            html = driver.page_source
            host = re.search(r'(https{0,1}://)(.+?)(/)', url).group(2)
            result = extractor.extract(html, host=host)
            content = result['content']
            sname = result['title']
            images = result['images']
        else:
            print(url, 'diffbot')
            sname = result['objects'][0]['siteName']
            text = result['objects'][0]['text']
            if 'images' in result['objects'][0]:
                imgs = result['objects'][0]['images']
                for img in imgs:
                    images.append(img['url'])

    return sname, content, images

goodURL = pd.read_csv("./good_url_5.1.csv")

del goodURL['Unnamed: 0']
Content = goodURL[:]

s,c,ims = [],[],[]
url_good = goodURL['url']
Content = goodURL[:]
n = len(url_good)
for i in range(n):
    url = url_good[i]
    print (url)
    sname,content,images = get_content(url,driver)
    s.append(sname)
    c.append(content)
    ims.append(images)
    if i==3:
        break