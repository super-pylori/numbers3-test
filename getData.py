from cmath import e
from tkinter import E
from bs4 import BeautifulSoup
import requests
import pandas as pd
from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

# 開始
start_time = time.perf_counter()

url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/numbers3/index.html?year=2021&month=5'

op = Options()
op.add_argument('--headless') # ブラウザを出さない
op.add_argument('--disable-gpu')                      
op.add_argument('--disable-extensions')               
op.add_argument('--proxy-server="direct://"')         
op.add_argument('--proxy-bypass-list=*')              
op.add_argument('--blink-settings=imagesEnabled=false')
op.add_argument('--lang=ja')                          
op.add_argument('--no-sandbox')
op.add_argument('--disable-dev-shm-usage')
op.add_argument("--log-level=3")
op.add_argument('--ignore-certificate-errors')
op.add_argument('--ignore-ssl-errors')
op.add_argument("--window-size=1440,1080")
op.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36')
op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option('excludeSwitches', ['enable-logging'])
op.add_experimental_option('useAutomationExtension', False)
# op.add_experimental_option("detach", True) # ブラウザ出るモードの時処理終了後もブラウザを閉じない
op.page_load_strategy = 'eager'

# （A表）先月から過去1年間の当せん番号　のリンクを格納した配列を返す
def get_tableA_links():
    for i in range(0, 3):
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            break

    url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/backnumber/index.html'
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "ナンバーズ3")))
    except Exception as e:
        time.sleep(10)

    lists = []
    links = driver.find_elements_by_partial_link_text('ナンバーズ3')
    for link in links:
        lists.append(link.get_attribute('href'))
        if len(lists) == 12:
            break 
    return lists

# A表内リンクから回別、抽選日、抽選数字をDataFrameに変換
def get_data_from_tableA(tableA_links):
    for i in range(0, 3):
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            break

    backnumbers = []
    for link in tableA_links:
        url = link
        print(url)

        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[text()='ストレート']")))
        except Exception as e:
            time.sleep(10)        
        
        no = driver.find_elements_by_class_name('bgf7f7f7')
        date = driver.find_elements_by_class_name('js-lottery-date-pc')
        number = driver.find_elements_by_class_name('js-lottery-number-pc')

        for i in range(0,len(no)):
            backnumber = {}
            backnumber['回別'] = no[i].text
            backnumber['抽せん日'] = date[i].text
            backnumber['ナンバーズ3抽せん数字'] = number[i].text
            backnumbers.append(backnumber)

    return backnumbers

# （B表）A表以前の当せん番号　のリンクを格納した配列を返す
def get_tableB_links():
    for i in range(0, 3):
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            break

    url = 'https://www.mizuhobank.co.jp/retail/takarakuji/check/numbers/backnumber/index.html' 
    driver.get(url)

    try:
        WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "第1回〜第20回")))
    except Exception as e:
        time.sleep(10)

    lists = []
    links = driver.find_elements_by_xpath("//*[@class='js-backnumber-temp-b']/td/a")
    for link in links:
        if link.get_attribute('href') == "":
            continue
        lists.append(link.get_attribute('href'))
    
    return lists

# B表内リンクから回別、抽選日、抽選数字をDataFrameに変換
def get_data_from_tableB(tableB_links):
    for i in range(0, 3):
        try:
            driver = webdriver.Chrome(ChromeDriverManager().install(),options=op)
        except Exception as e:
            print(e)
            time.sleep(5)
        else:
            break

    backnumbers = []
    for link in tableB_links:
        url = link
        print(url)

        driver.get(url)

        try:
            WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='mainCol']/article/div[1]/div/div[1]/table/tbody/tr[20]/th")))
        except Exception as e:
            time.sleep(10)

        # html = driver.page_source
        # with open('hoge.html', 'w', encoding='utf-8') as f:
        #     f.write(html)

        no = driver.find_elements_by_xpath("//table[@class='typeTK']/tbody/tr/th[@class='bgf7f7f7']")
        date = driver.find_elements_by_xpath("//table[@class='typeTK']/tbody/tr/th[@class='bgf7f7f7']/following-sibling::td[1]")
        number = driver.find_elements_by_xpath("//table[@class='typeTK']/tbody/tr/th[@class='bgf7f7f7']/following-sibling::td[2]")

        for i in range(0,len(no)):
            backnumber = {}
            backnumber['回別'] = no[i].text
            backnumber['抽せん日'] = date[i].text
            backnumber['ナンバーズ3抽せん数字'] = number[i].text
            backnumbers.append(backnumber)

    return backnumbers[::-1]

tableA_links = get_tableA_links()
backnumbersA = get_data_from_tableA(tableA_links)
backnumbersA_df = pd.DataFrame(backnumbersA)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(backnumbersA_df)

backnumbersA_df.to_csv('numbers3.csv')
exit()

tableB_links = get_tableB_links()
backnumbersB = get_data_from_tableB(tableB_links)
backnumbersB_df = pd.DataFrame(backnumbersB)
with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(backnumbersB_df)

df = pd.DataFrame()
df = pd.concat([backnumbersA_df,backnumbersB_df], ignore_index=True)

# 空白行の削除
df = df.dropna(how='all')

df.to_csv('numbers3.csv')

# 終了
end_time = time.perf_counter()

print(start_time)
print(end_time)
print(end_time - start_time)