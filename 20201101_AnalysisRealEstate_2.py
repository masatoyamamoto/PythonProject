import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 分析
df = pd.read_csv("./Data/Data.csv",  encoding="utf-8")
summary = df.describe()
ku_group = df.groupby("ku")
count_by_ku = ku_group.size()
plt.bar(count_by_ku.index,count_by_ku)
