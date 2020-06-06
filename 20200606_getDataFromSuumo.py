# Libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from pandas import Series, DataFrame
import time
import csv
import slackweb as sw


def getSuumo(url):
    # データ取得
    result = requests.get(url).content

    # HTMLを元にオブジェクトを作る
    soup = BeautifulSoup(result, 'lxml')

    # 物件リストを切り出し、必要データを抜き出す。現在の構造にかなり依存したとり方
    summary = soup.find("div", {'id': 'js-bukkenList'})
    summary_2 = summary.find_all("div", {"class": "dottable-line"})

    bukken_result = list()

    for i in summary_2:
        data = i.find_all("dd")
        # 空でなければ
        if data:
            for j in data:
                bukken_result.append(j.text.replace("\n", ""))

    # numpy化して折り返す
    np_result = np.array(bukken_result).reshape(int(len(bukken_result) / 8), 8)

    # データフレームに変換
    column = ["name", "price", "location", "station", "size", "floor", "terrace", "age"]
    df_SuumoData = pd.DataFrame(np_result, columns=column)
    return (df_SuumoData)


# ####################################################

# 最初のurlを指定したら、全てのページに対してデータを取りに行く関数
def getSuumoDataFromAllPages(url):
    # ページ数取得 もっと良い方法がありそう。
    soup = BeautifulSoup(requests.get(url).content, 'lxml')
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

    # データを入れるdf
    SuumoData = getSuumo(url)

    # 2ページ目から最後のページまでを格納
    for i in range(pages_split3 - 1):
        pg = str(i + 2)
        url_page = url + '&pn=' + pg
        urls.append(url_page)

    # 各ページに対して処理していく

    for i in range(len(urls) - 1):
        kekka = getSuumo(urls[i + 1])

        SuumoData = SuumoData.append(kekka, ignore_index=True)
        print("...")

        time.sleep(10)

    SuumoData.to_csv("suumoData.csv", encoding="utf-16")


# url = "https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13101&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1"
# getSuumoDataFromAllPages(url)

# 全ての地域を選択したURL
url = "https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13101&sc=13102&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13201&sc=13202&sc=13203&sc=13204&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&kb=1&kt=9999999&mb=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1"
getSuumoDataFromAllPages(url)

slack = sw.Slack(url="https://hooks.slack.com/services/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")
slack.notify(text="処理が終わりました")
