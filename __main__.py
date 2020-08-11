from datetime import datetime
from itertools import count
from bs4 import BeautifulSoup
from selenium import webdriver
import time

from collection import crawler
import pandas as pd


def crawling_pelicana():
    results = []

    for page in range(start=1, step=1):
        url = 'https://pelicana.co.kr/store/stroe_search.html?branch_name=&gu=&si=&page=%d' % page
        html = crawler.crawling(url)
        bs = BeautifulSoup(html, 'html.parser')
        tag_table = bs.find('table', attrs={'class':['table', 'mt20']})
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')

        if len(tags_tr) == 0:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[3]
            sidogu = address.split()[0:2]
            t = (name, address) + tuple(sidogu)
            results.append(t)

    # store
    table = pd.DataFrame(results,columns=['name','address','sido','gigun'])
    table.to_csv('results/pelicana.csv', encoding='utf-8',mode="w", index=True)


def crawling_nene():
    results = []
    prev_name = ""
    for page in count(1,1):
        url = 'https://nenechicken.com/17_new/sub_shop01.asp?ex_select=1&ex_select2=&IndexSword=&GUBUN=A&page=%d' % page
        html = crawler.crawling(url)

        bs = BeautifulSoup(html, 'html.parser')
        tags_div = bs.findAll('div',attrs={'class':'shopInfo'})

        fin_flag = False
        print(prev_name)
        for index, tag_div in enumerate(tags_div):

            strings = list(tag_div.strings)
            name = strings[4]
            address = strings[6]
            if index == 0 and prev_name == name:
                fin_flag = True
                break
            if index == 0 and prev_name != name:
                prev_name = name
            sidogu = address.split()[0:2]
            t = (name, address) + tuple(sidogu)
            results.append(t)

        if fin_flag is True:
            break
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gigun'])
    table.to_csv('results/nene.csv', encoding='utf-8', mode="w", index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        for sido2 in count(start=1, step=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1,sido2)
            html = crawler.crawling(url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})
            tags_span = tag_ul.findAll('span', attrs={'class': 'store_item'})

            for tag_span in tags_span:
                strings = list(tag_span.strings)
                name = strings[1]
                address= strings[3].strip('\r\n\t')

                sidogu = address.split()[0:2]
                t = (name, address)+tuple(sidogu)
                results.append(t)

    table = pd.DataFrame(results,columns=['name','address','sido','gigun'])
    table.to_csv('results/kyochob.csv', encoding='utf-8',mode="w", index=True)


def crawling_goobne():
    url = 'http://www.goobne.co.kr/store/search_store.jsp'

    # 첫 페이지 로딩
    wd = webdriver.Chrome('C:\\gachon2020\\chromedriver.exe')
    wd.get(url)
    time.sleep(3)

    # 자바스크립트 실행
    script = 'store.getList(2)'
    wd.execute_script(script)
    print(f'{datetime.now()} : success for request[{script}]')
    time.sleep(2)

    # 자바스크립트 실행결과(동적으로 렌더링된 HTML) 가져오기
    html = wd.page_source
    print(html)
    wd.quit()


if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene(과제)
    #crawling_nene()

    # kyochon
    #crawling_kyochon()

    # goobne
    crawling_goobne()