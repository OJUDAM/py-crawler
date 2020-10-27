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


def crawling_wiki():
    results = []
    urldd = 'https://ko.wiktionary.org/wiki/%EB%B6%84%EB%A5%98:%ED%95%9C%EA%B5%AD%EC%96%B4_%EB%AA%85%EC%82%AC'

    def crawling_data(url):

        html = crawler.crawling(url)
        bs = BeautifulSoup(html, 'html.parser')

        #단어 parsing
        tag_div_id = bs.find('div', attrs={'id': 'mw-pages'})
        tag_div = tag_div_id.find('div', attrs={'class': 'mw-category-group'})
        tag_ul = tag_div.find('ul')
        tags_a = tag_ul.findAll('a')

        for a in tags_a:
            t = a.get('title')
            if len(t) > 1:
                results.append(t)
            else:
                continue

            if a == "흰죽":
                return "end"


        # 다음 페이지 url 알아내기
        tag_div_page = bs.find('div', attrs={'id': 'mw-pages'})
        next_pages = tag_div_page.findAll('a', attrs={'title': '분류:한국어 명사'})
        list_page = list(next_pages)
        next_url = 'https://ko.wiktionary.org/'+list_page[-1].get('href')
        return next_url

    next = urldd
    index = 0
    while index < 131:
        next = crawling_data(next)
        index += 1

    table = pd.DataFrame(results, columns=['word'])
    table.to_csv('results/wiki.csv', encoding='utf-8', mode="w", index=True)




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

    results = []
    for page in count(1, 1):
        # 자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)
        print(f'{datetime.now()} : success for request[{script}]')
        time.sleep(2)

        # 자바스크립트 실행결과(동적으로 렌더링된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody= bs.find('tbody', attrs={'id': 'store_list'})
        tags_tr = tag_tbody.findAll('tr')

        # 끝 검출
        if tags_tr[0].get('class') is None:
            break

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[0:2]
            t = (name, address) + tuple(sidogu)
            results.append(t)

    print(results)
    wd.quit()

    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gigun'])
    table.to_csv('results/goobne.csv', encoding='utf-8', mode="w", index=True)


if __name__ == '__main__':
    # pelicana
    # crawling_pelicana()

    # nene(과제)
    #crawling_nene()

    # kyochon
    #crawling_kyochon()

    # goobne
    #crawling_goobne()

    # wiki
    crawling_wiki()