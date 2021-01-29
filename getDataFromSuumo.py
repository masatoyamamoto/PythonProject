from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import pandas as pd
import datetime
from pandas import DataFrame


# suumoからデータを取得してpandasのDataFrameを返す関数。
def get_suumo(url_to_suumo: str):
    # データ取得
    result = requests.get(url_to_suumo).content
    soup = BeautifulSoup(result, 'lxml')  # HTMLを元にオブジェクトを作る
    summary = soup.find("div", {'id': 'js-bukkenList'})  # 物件リストを切り出し、必要データを抜き出す。現在の構造にかなり依存したとり方
    summary_2 = summary.find_all("div", {"class": "dottable-line"})

    bukken_result: list = list()
    for i in summary_2:
        data = i.find_all("dd")
        # 空でなければ
        if data:
            for j in data:
                bukken_result.append(j.text.replace("\n", ""))
    # numpy化して折り返す
    try:
        np_result: np = np.array(bukken_result).reshape(int(len(bukken_result) / 8), 8)
    except Exception:
        np_result = np.array(np.repeat("-", 8).reshape(1, 8))
    # データフレームに変換
    column = ["name", "price", "location", "station", "size", "floor", "terrace", "construction"]
    df_suumo_data: DataFrame = pd.DataFrame(np_result, columns=column)

    return df_suumo_data


# 最初のurlを指定したら、全てのページに対してデータを取りに行く関数
def get_suumo_data_from_all_pages(url_in_get_data: str):
    # ページ数取得 もっと良い方法がありそう。
    soup = BeautifulSoup(requests.get(url_in_get_data).content, 'lxml')
    body = soup.find("body")
    pages = body.find_all("div", {'class': 'pagination pagination_set-nav'})
    pages_text = str(pages)
    pages_split = pages_text.split('</a></li>\n</ol>')
    pages_split0 = pages_split[0]
    pages_split1 = pages_split0[-3:]
    pages_split2 = pages_split1.replace('">', '')
    pages_split3 = int(pages_split2)

    # URLを入れるリスト
    urls = [url_in_get_data]

    # データを入れるdf
    suumo_data = get_suumo(url_in_get_data)

    # 2ページ目から最後のページまでを格納
    for i in range(pages_split3 - 1):
        pg = str(i + 2)
        url_page = url + '&pn=' + pg
        urls.append(url_page)

    # 各ページに対して処理していく

    for i in range(len(urls) - 1):
        the_result = get_suumo(urls[i + 1])

        suumo_data = suumo_data.append(the_result, ignore_index=True)
        print("...")
        print(str(i + 1) + "ページ目が終わりました")

        time.sleep(10)

    return suumo_data


def data_amend(df: DataFrame):
    # df = pd.read_csv("./Data/suumoData.csv", encoding="utf-8")  # データ読み込み

    # 路線、駅名、徒歩時間を切り分ける
    df_split_1 = df["station"].str.split("歩", expand=True)
    df_split_1 = pd.concat([df_split_1[0].str.split("「", expand=True), df_split_1[1]], axis=1)
    df_split_1.columns = ["line", "station", "time"]
    df_split_1["station"] = df_split_1["station"].str.replace("」(.)", "")  # いらない文字を削除
    df_split_1["time"] = df_split_1["time"].str.replace("分", "")
    df.drop(['station'], axis=1, inplace=True)  # 切り分けたので元データを削除

    # 住所を修正。東京23区内のみの分析にする。
    df = df[df["location"].str.contains("区")]
    temp_1 = df["location"].str.replace("東京都", "").str.split("区", expand=True)
    temp_1.columns = ["ku", "address"]
    df = pd.concat((df, temp_1), axis=1)

    # 広さのm2以降を削除する
    df["size"] = df["size"].replace("m2(.*)", "", regex=True)
    df["terrace"] = df["terrace"].replace("m2(.*)", "", regex=True)

    # 価格を使えるデータに整形する
    df = df[~df["price"].str.contains("~|〜|・|〜|～|※")]  # 注釈とか幅をもたせたデータは削除
    df_split_1 = pd.DataFrame(df["price"].str.extract('(.*億)')[0].str.replace("億", "").fillna(0).astype(
        int) * 10000)  # 億円以上の部分は10,000かけて単位をずらす。intに変換
    df_split_2 = pd.DataFrame(
        df["price"].str.replace('(.*億)', "").str.replace("万|円", "").str.extract(r"(\d+)").fillna(0).astype(int))
    df["price"] = df_split_1 + df_split_2  # 万円の数字に変換

    # 建築日を使えるデータにする
    df["construction"] = pd.to_datetime(df["construction"] + "1日", format="%Y年%m月%d日")
    temp_1 = pd.to_datetime(dt.date.today()) - df["construction"]
    temp_1 = temp_1.rename(columns={"construction": "age"})
    df = pd.concat((df, temp_1), axis=1)

    # floorの修正
    temp_1 = pd.Series(df["floor"]).str.replace("(.*ワンルーム)", "1")
    rldks: DataFrame = pd.DataFrame([
        temp_1.str.extract(r"(\d\d*)")[0],
        temp_1.str.count("L"),
        temp_1.str.count("D"),
        temp_1.str.count("K"),
        temp_1.str.extract(r"(\+.*S)")[0].fillna("0").str.extract(r"(\d+)").fillna(1)[0]],
        index=["room", "Living", "Dining", "Kitchen", "Service"]).astype(int).T
    temp2 = pd.DataFrame({"No.ofRooms": rldks.sum(axis=1)})

    df = pd.concat((df, rldks, temp2), axis=1)

    # 出力
    df_result: pd = df[
        ["name", "size", "terrace", "age_1", "ku", "room", "Living", "Dining", "Kitchen", "Service", "No.ofRooms",
         "price"]]
    # df_result.to_csv("Data.csv", encoding="utf-8")
    return df_result


# 全ての地域を選択したURL 800ページくらいあるのでめっちゃ時間がかかる。
url = "https://suumo.jp/jj/bukken/ichiran/JJ010FJ001/?ar=030&bs=011&ta=13&jspIdFlg=patternShikugun&sc=13101&sc=13102" \
      "&sc=13103&sc=13104&sc=13105&sc=13113&sc=13106&sc=13107&sc=13108&sc=13118&sc=13121&sc=13122&sc=13123&sc=13109" \
      "&sc=13110&sc=13111&sc=13112&sc=13114&sc=13115&sc=13120&sc=13116&sc=13117&sc=13201&sc=13202&sc=13203&sc=13204" \
      "&sc=13205&sc=13206&sc=13207&sc=13208&sc=13209&sc=13210&sc=13211&sc=13212&sc=13213&sc=13214&sc=13215&sc=13218" \
      "&sc=13219&sc=13220&sc=13221&sc=13222&sc=13223&sc=13224&sc=13225&sc=13227&sc=13228&sc=13229&kb=1&kt=9999999&mb" \
      "=0&mt=9999999&ekTjCd=&ekTjNm=&tj=0&cnb=0&cn=9999999&srch_navi=1 "

temp = get_suumo_data_from_all_pages(url)
temp = data_amend(temp)
temp.to_csv("./Data/Suumo_" + datetime.date.today().strftime("%Y-%M-%D") + ".csv", index=False)
