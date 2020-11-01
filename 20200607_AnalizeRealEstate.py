import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# データ読み込み
df = pd.read_csv("suumoData.csv", sep="\t", encoding="utf-16")
# 不要な列を削除
df.drop(['Unnamed: 0'], axis=1, inplace=True)

# 路線、駅名、徒歩時間を切り分ける
df_split_1 = df["station"].str.split("歩", expand=True)
df_split_1 = pd.concat([df_split_1[0].str.split("「", expand=True), df_split_1[1]], axis=1)
df_split_1.columns = ["line", "station", "time"]
# いらない文字を削除
df_split_1["station"] = df_split_1["station"].str.replace("」(.)", "")
df_split_1["time"] = df_split_1["time"].str.replace("分", "")
# 切り分けたので元データを削除
df.drop(['station'], axis=1, inplace=True)
df = pd.concat([df, df_split_1], axis=1)

# 広さのm2等を削除する
df["size"] = df["size"].replace("m2(.*)", "", regex=True)
df["terrace"] = df["terrace"].replace("m2(.*)", "", regex=True)

# 値段を扱いやすくする。
df = df[~df["price"].str.contains("~")]
df = df[~df["price"].str.contains("-")]
df = df[~df["price"].str.contains("～")]
df = df[~df["price"].str.contains("※")]
df = df[~df["price"].str.contains("・")]

# いっそ1億円以上は分析対象外(20200927）
df = df[~df["price"].str.contains("億")]
df["price"] = df["price"].replace("万円", "0000", regex=True)

# 数値データの-を0に変換
df["size"] = df["size"].replace("-", 0)
df["terrace"] = df["terrace"].replace("-", 0)

# 23区内に分析対象を限定
df = df[~df["location"].str.contains("市")]
df_split_1 = df["location"].str.split("区", expand=True)
df_split_1.columns = ["ku", "cho-son"]
df = pd.concat([df, df_split_1], axis=1)
df.drop(["location"], axis=1, inplace=True)
df["ku"] = df["ku"].replace("東京都", "", regex=True)

# 前処理の記録
df.to_csv("sumoAnalyze.csv", encoding="utf-16")

