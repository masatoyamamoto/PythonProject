# 必要なライブラリをインポート
from bs4 import BeautifulSoup
import requests
import pandas as pd
from pandas import Series, DataFrame
import time
import slackweb as sw

slack = sw.Slack(url="https://hooks.slack.com/services/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")
slack.notify(text="処理が終わりました")
