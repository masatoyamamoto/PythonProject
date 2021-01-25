import pandas as pd
import datetime as dt
import numpy as np


df = pd.read_csv("./Data/suumoData.csv",  encoding="utf-8")  # データ読み込み

# 路線、駅名、徒歩時間を切り分ける
df_split_1 = df["station"].str.split("歩", expand=True)
df_split_1 = pd.concat([df_split_1[0].str.split("「", expand=True), df_split_1[1]], axis=1)
df_split_1.columns = ["line", "station", "time"]
# いらない文字を削除
df_split_1["station"] = df_split_1["station"].str.replace("」(.)", "")
df_split_1["time"] = df_split_1["time"].str.replace("分", "")
# 切り分けたので元データを削除
df.drop(['station'], axis=1, inplace=True)

# 広さのm2等を削除する
df["size"] = df["size"].replace("m2(.*)", "", regex=True)
df["terrace"] = df["terrace"].replace("m2(.*)", "", regex=True)

# 価格を使えるデータに整形する
df = df[~df["price"].str.contains("~|〜|・|〜|～|※")]  # 注釈とか幅をもたせたデータは削除

# 億円以上の部分
df_split_1 = df["price"].str.extract('(.*億)')[0].str.replace("億","").fillna(0).astype(int)

df.to_csv("test.csv")


