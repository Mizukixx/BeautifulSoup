#coding:utf-8
PURPLE  = '\033[35m'
RED     = '\033[31m'
CYAN    = '\033[36m'
OKBLUE  = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL    = '\033[91m'
ENDC    = '\033[0m'


import requests
import json
from bs4 import BeautifulSoup
from time import sleep
import re
import shutil


def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open('image/'+ file_name, 'wb') as f:
           r.raw.decode_content = True
           shutil.copyfileobj(r.raw, f)


user_agent = {'User-agent': 'Mozilla/5.0'}
r = requests.get('https://www.yamada-denkiweb.com/category/215/003/',headers = user_agent)
soup = BeautifulSoup(r.text , "html.parser") 


W = open('result.csv','w')
W.write('商品名,商品URL,価格,画像\n')
B = open('ID-img_url.csv', 'w')
B.write('id_num,img_url\n')
set_url = set()
list_img_url = []
for a in soup.find_all(class_='item-name'):
    a_tag = a.find_all('a')[0]
    target = "https://www.yamada-denkiweb.com"+a_tag.attrs['href']
    set_url.add(target)

num = 1
for i in set_url:
    id_num = num
    ID = i.split("https://www.yamada-denkiweb.com/")[1]
    r = requests.get(i)
    # r.textで文字化けしたので
    S = BeautifulSoup(r.content , "html.parser")
    
    #ID-number
    count = len(set_url)
    print("【"+str(id_num)+" / "+ str(count)+ "】")
    #URL
    print(OKBLUE+i+ENDC)
    #商品名
    title = S.find_all(class_="item-name set")[0].text.replace("\n","")
    print(title)
    #商品価格
    price = S.find_all(class_="highlight x-large")[0].text.replace("\n","")
    print(PURPLE+price+ENDC)

    #商品画像の取得
    num_id_sub = 0
    img_tag = ''
    a = S.find_all(class_="trigger")
    try:
        image = str(a).split('src="')[1].split('"')[0]
        print(OKGREEN+image+ENDC) #URL
        list_img_url.append(image)
        B.write(str(id_num)+','+str(image)+'\n')
        num_id_sub +=1
        file_name = str(ID)+'.jpg'
        download_img(str(image), file_name)
        img_tag = img_tag + ',' +file_name
        sleep(0.1)
    except:
        print('yes')
    print('=======================================')

    W.write(title.replace(',','')+","+i+","+price.replace(',','')+img_tag+'\n')
    sleep(0.5)
    num+=1
W.close()
B.close()
