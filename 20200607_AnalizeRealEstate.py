import pandas as pd
import numpy as np

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

