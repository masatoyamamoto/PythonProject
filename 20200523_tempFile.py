# Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import csv

# URL 試しに、千代田区の中古マンション購入の検索画面トップ
url = "https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13101&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1"

# データ取得
result = requests.get(url)
c = result.content

# HTMLを元にオブジェクトを作る
soup = BeautifulSoup(c, 'lxml')

# 物件リストを切り出し
summary = soup.find("div", {'id': 'js-bukkenList'})
dataSet = summary.find_all("table")
name = summary.find_all()
price = summary.find_all("span", {'class': 'dottable-value'})


a = 1
for i in dataSet:
    if a % 2 == 1: print(str(a/2+0.5) + '----------------------')
    a += 1
    rows = i.find_all("tr")

    for j in rows:
        row = j.find_all("dd")
        for k in row:
            print(k.text)
    print(price[a-1].text)

# print(summary.prettify())
