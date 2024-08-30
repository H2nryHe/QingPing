import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
}
params = {
    'type': "concept"
}
# <span class="hljs-string">'https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/plate?'</span>
# url = 'https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/plate?'
url = 'https://dq.10jqka.com.cn/fuyao/hot_list_data/out/hot_list/v1/stock?stock_type=a&type=day&list_type=trend'
# url = 'https://eq.10jqka.com.cn/frontend/thsTopRank/index.html?tabName=redian&client_userid=zSTQZ&share_hxapp=gsc&share_action=&back_source=wxhy#/'
response = requests.get(url=url, params=params, headers=headers)
print(response.status_code)
# html = response.text
# print('here starts:')
# print(html)
res = response.json()
# print('\n')
print(res)
# soup = BeautifulSoup(html, 'html.parser')
# # <span data-v-2e888cf8="" class="ellipsis" style="max-width: 100%; line-height: 0.34rem;">深圳华强</span>
# stock_names = soup.find_all('span', attrs={'class': 'ellipsis'})
# # <div data-v-2e888cf8="" class="bold THSMF-M flex ai-c ellipsis range" style="width: 1.8rem; font-size: 0.32rem; color: rgb(255, 36, 54); justify-content: flex-end;">+10.02%</div>
# change_price = soup.find_all('div', attrs={'class': 'bold THSMF-M flex ai-c ellipsis range'})

# print(len(stock_names))
# print("same length" if len(stock_names) == len(change_price) else "not same length")
# df = pd.DataFrame([stock_names, change_price])
# print(df.head())
df = pd.DataFrame(res['data']['stock_list'])
df = df.rename(columns={'code': '概念代码', 'name': '概念名称'})
print(df.head())
df.to_csv('hot_stock_data_8_30.csv', index=False, encoding='utf-8')
