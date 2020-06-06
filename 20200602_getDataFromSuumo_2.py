# Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import csv

# URL 試しに、千代田区の中古マンション購入の検索画面トップ
url = "https://suumo.jp/jj/bukken/ichiran/JJ012FC002/?ar=030&bs=011&cn=9999999&cnb=0&ekTjCd=&ekTjNm=&kb=1&kt=9999999&mb=0&mt=9999999&sc=13101&ta=13&tj=0&bknlistmodeflg=2&pc=30&pn=1"

# データ取得
result = requests.get(url)
c = result.content

# HTMLを元にオブジェクトを作る
soup = BeautifulSoup(c, 'lxml')

summary = soup.find("div", {'id': 'js-bukkenList'})

bukkenData = summary.find_all("div", {"class": "property_unit-content"})
bukken_1 = bukkenData[0]

# まずは物件毎のデータ取得
title = bukken_1.find("h2", {"class": "property_unit-title_wide"}).find("a").text
dataSet = bukken_1.find_all("table")

a = 1
for i in dataSet:
    # if a % 2 == 1: print(str(a/2+0.5) + '----------------------')
    a += 1
    rows = i.find_all("dd")
    for j in rows:
        print(":")
        print(j.text)
