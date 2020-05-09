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

# ページ数取得 もっと良い方法がありそう。
body = soup.find("body")
pages = body.find_all("div", {'class': 'pagination pagination_set-nav'})
pages_text = str(pages)
pages_split = pages_text.split('</a></li>\n</ol>')
pages_split0 = pages_split[0]
pages_split1 = pages_split0[-3:]
pages_split2 = pages_split1.replace('">', '')
pages_split3 = int(pages_split2)

# URLを入れるリスト
urls = [url]

# 2ページ目から最後のページまでを格納
for i in range(pages_split3 - 1):
    pg = str(i + 2)
    url_page = url + '&pn=' + pg
    urls.append(url_page)

name = []  # マンション名
address = []  # 住所
locations0 = []  # 立地1つ目（最寄駅/徒歩~分）
locations1 = []  # 立地2つ目（最寄駅/徒歩~分）
locations2 = []  # 立地3つ目（最寄駅/徒歩~分）
age = []  # 築年数
height = []  # 建物高さ
floor = []  # 階
rent = []  # 賃料
admin = []  # 管理費
others = []  # 敷/礼/保証/敷引,償却
floor_plan = []  # 間取り
area = []  # 専有面積

# 各ページで以下の動作をループ
for url in urls:
    # 物件リストを切り出し
    result = requests.get(url)
    c = result.content
    soup = BeautifulSoup(c)
    summary = soup.find("div", {'id': 'js-bukkenList'})

    # マンション名、住所、立地（最寄駅/徒歩~分）、築年数、建物高さが入っているcassetteitemを全て抜き出し
    cassetteitems = summary.find_all("div", {'class': 'cassette'})



