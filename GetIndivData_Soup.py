# -*- coding: utf-8 -*-
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time
from bs4 import BeautifulSoup

import copy
import pandas as pd
import numpy as np
import csv
import sys

def GetShopData(href, driver, df, first):

	try:
		if first == True:
			# 取得先URLにアクセス
			driver.get(href)
		
		page_source = driver.page_source
		soup = BeautifulSoup(page_source, 'html.parser')

		'''
		# コンテンツが描画されるまで待機
		about = driver.find_elements_by_link_text('次へ')
		about[0].click()
		'''
		time.sleep(5)

		lst = soup.find_all('ul', class_ = 'ulDotList')
		if len(lst) > 0:
			contents = lst[0].find_all('li')

			for content in contents:
				dataname = []
				datavalue = []

				if '〒' in content.text:
					elems = content.find_all('p')
					for i in range(len(elems)): 
						elem = elems[i].text.replace('\n', '').replace('\t', '')
						if i == 0:
							dataname.append('会社名')
							datavalue.append(elem)
							company_link = elems[i].find_all('a')
							if len(company_link) > 0:
								company_url = company_link[0].get('href')
								dataname.append('ホームページ')
								datavalue.append(company_url)
						if '〒' in elem:
							dataname.append('住所')
							datavalue.append(elem)
						if 'TEL' in elem:
							dataname.append('TEL')
							if 'FAX' in elem:
								dataname.append('FAX')
								tel = elem.split('FAX：')[0].replace('TEL：', '')
								fax = elem.split('FAX：')[1]
								datavalue.append(tel)
								datavalue.append(fax)
							else:
								datavalue.append(elem.replace('TEL：', ''))
						if 'E-mail' in elem:
							dataname.append('E-mail')
							datavalue.append(elem.replace('E-mail：', ''))
						if '保険付保実績数' in elem:
							dataname.append('保険付保実績数')
							datavalue.append(elems[i+1].text)

					dataser = pd.Series(datavalue, index = dataname)
					df = df.append(dataser, ignore_index = True)

			more = driver.find_elements_by_partial_link_text('次へ')
			if len(more) > 0:
				more[0].click()
				df = GetShopData(href, driver, df, False)

	except:
		print(traceback.format_exc())
		df = GetShopData(href, driver, df, True)

	return df


def GetCityList(pref):

	url = 'https://www.j-anshin.co.jp/list_todokede/zip_list.php?mode=area&search_key=' + pref

	indivurl = 'https://www.j-anshin.co.jp/list_todokede/search_list.php?mode=area&search_key='
	indivurl2 = '&search_key2=' + pref

	driver.get(url)
	time.sleep(2)

	hrefs = []

	cities = driver.find_elements_by_css_selector('ul > li > div > a')
	for city in cities:
		href = indivurl + city.text + indivurl2
		hrefs.append(href)

	return hrefs


if __name__ == '__main__':

	# url = 'https://suumo.jp/chumon/tn_hokkaido/rn_cleverlyhome/?ichiranIdx=1'
	options = Options()
	# ヘッドレスモードで実行する場合
	# options.add_argument("--headless")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(10)


	prefs = ['北海道', '青森県', '岩手県', '宮城県', '秋田県', '山形県', '福島県', '茨城県', '栃木県', '群馬県', \
			'埼玉県', '千葉県', '東京都', '神奈川県', '山梨県', '新潟県', '長野県', '富山県', '石川県' , '福井県', \
			'静岡県', '愛知県', '三重県', '岐阜県', '滋賀県', '京都府', '大阪府', '兵庫県', '奈良県', '和歌山県', \
			'鳥取県', '島根県', '岡山県', '広島県', '山口県', '香川県', '徳島県', '愛媛県', '高知県', '福岡県', \
			'佐賀県', '長崎県', '熊本県', '大分県', '宮崎県', '鹿児島県', '沖縄県']


	columns = ['会社名', '住所', 'TEL', 'FAX', 'E-mail', '保険付保実績数', 'ホームページ']

	df = pd.DataFrame(index = [], columns = columns)

	for pref in prefs:
	
		hrefs = GetCityList(pref)

		for href in hrefs:
			df = GetShopData(href, driver, df, True)

	df.to_csv('data.csv', index=None, encoding='cp932')
	driver.close()





	'''
	# url = 'https://suumo.jp/chumon/tn_hokkaido/rn_cleverlyhome/?ichiranIdx=1'
	options = Options()
	# ヘッドレスモードで実行する場合
	# options.add_argument("--headless")
	driver = webdriver.Chrome(options=options)
	driver.implicitly_wait(10)

	columns = ['', '会社名', '所在地', '設立', '問い合わせ', '資本金', '従業員数', '施工エリア', '施工実績', '対応可能工法', 'アフター・保証', 'ホームページ', '参考価格']

	df = pd.DataFrame(index = [], columns = columns)

	# urllist = AccumulateUrl(driver)

	f = open('urllist2.csv', 'w')
	for url in urllist:
		f.write(url)
		f.write("\n")
	f.close()

	# driver.close()
	# sys.exit()

	with open('urllist2.csv') as f:
		reader = csv.reader(f)
		for url in reader:
			df = GetShopData(url[0], driver, df)

	df.to_csv('data2.csv', index=None, encoding='cp932')
	driver.close()
	'''