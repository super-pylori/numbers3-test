from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/numbers3/index.html?year=2021&month=5'

op = Options()
op.add_argument("--headless");
op.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36')
op.add_argument('--lang=ja-JP')

# （A表）先月から過去1年間の当せん番号　のリンクを格納した配列を返す
def backnumber_latest_link_to_lists():
    url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/backnumber/index.html'

    driver = webdriver.Chrome('/usr/bin/chromedriver',options=op)
    driver.get(url)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,'html.parser')
    
    lists = []
    links = driver.find_elements_by_partial_link_text('ナンバーズ3')
    for link in links:
        lists.append(link.get_attribute('href'))
    
    return lists


backnumber_latest = backnumber_latest_link_to_lists()

# A表から回別、抽選日、抽選数字をDataFrameに変換　
backnumbers = []
for link in backnumber_latest:
    url = link

    driver = webdriver.Chrome('/usr/bin/chromedriver',options=op)
    driver.get(url)
    no = driver.find_elements_by_class_name('bgf7f7f7')
    date = driver.find_elements_by_class_name('js-lottery-date-pc')
    number = driver.find_elements_by_class_name('js-lottery-number-pc')


    for i in range(0,len(no)):
        backnumber = {}
        backnumber['回別'] = no[i].text
        backnumber['抽せん日'] = date[i].text
        backnumber['ナンバーズ3抽せん数字'] = number[i].text

        backnumbers.append(backnumber)

        print(no[i].text)

backnumber_df = pd.DataFrame(backnumbers)

