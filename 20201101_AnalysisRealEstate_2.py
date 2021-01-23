import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 分析
df = pd.read_csv("sumoAnalyze.csv",  encoding="utf-16")
df.drop(['Unnamed: 0'], axis=1, inplace=True)
summary = df.describe()

