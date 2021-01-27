import pandas as pd
import datetime as dt

df = pd.read_csv("./Data/suumoData.csv", encoding="utf-8")  # データ読み込み

# 路線、駅名、徒歩時間を切り分ける
df_split_1 = df["station"].str.split("歩", expand=True)
df_split_1 = pd.concat([df_split_1[0].str.split("「", expand=True), df_split_1[1]], axis=1)
df_split_1.columns = ["line", "station", "time"]
df_split_1["station"] = df_split_1["station"].str.replace("」(.)", "")  # いらない文字を削除
df_split_1["time"] = df_split_1["time"].str.replace("分", "")
df.drop(['station'], axis=1, inplace=True)  # 切り分けたので元データを削除

# 住所を修正。東京23区内のみの分析にする。
df = df[df["location"].str.contains("区")]
temp = df["location"].str.replace("東京都", "").str.split("区", expand=True)
temp.columns = ["ku", "address"]
df = pd.concat((df, temp), axis=1)

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
# df["construction"] = pd.to_datetime(df["construction"] + "1日", format="%Y年%m月%d日")
# temp = pd.to_datetime(dt.date.today()) - df["construction"]
df["age"] = pd.to_datetime(df["age"] + "1日", format="%Y年%m月%d日")
temp = pd.DataFrame(pd.to_datetime(dt.date.today()) - df["age"])
temp = temp.rename(columns={"age": "age_1"})
df = pd.concat((df, temp), axis=1)

# floorの修正
temp = pd.Series(df["floor"]).str.replace("(.*ワンルーム)", "1")
rldks = pd.DataFrame([
    temp.str.extract(r"(\d\d*)")[0],
    temp.str.count("L"),
    temp.str.count("D"),
    temp.str.count("K"),
    temp.str.extract(r"(\+.*S)")[0].fillna("0").str.extract(r"(\d+)").fillna(1)[0]],
    index=["room", "Living", "Dining", "Kitchen", "Service"]).astype(int).T
temp2 = pd.DataFrame({"No.ofRooms": rldks.sum(axis=1)})
df = pd.concat((df, rldks,temp2), axis=1)

# 出力
df_result: pd = df[["name", "size", "terrace", "age_1","ku", "room", "Living", "Dining", "Kitchen", "Service", "No.ofRooms", "price"]]
df_result.to_csv("Data.csv", encoding="utf-8")
