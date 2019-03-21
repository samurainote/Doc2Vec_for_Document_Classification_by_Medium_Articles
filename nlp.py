
import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

"""
取得したい記事のタグ一覧
Data Science
Artificial Intelligence
Machine Learning
Deep Learning
Neural Networks
"""

"""
作りたいデータテーブルのカラム一覧
index
title
link
author
publication
date
reading_time
clap
tag
"""


"""URLの準備"""

# スクレイピング対象のurlを作成
def tag_url_builder(tag):
    # MediumのArchiveの構造例 "https://medium.com/tag/deep-learning/archive/2018/01/13"
    tag_url = "https://medium.com/tag/" + tag + "/archive/"
    return tag_url


def get_start_date(year, month, day):
    #CHECKS IF START DATE IS A VALID DATE, CONVERTS TO DATETIME OBJECT
    try:
        start_date = datetime(year, month, day)
    except:
        raise Exception("Start date is in the wrong format or is invalid.")
    return start_date

def get_end_date(year, month, day):
    #CHECKS IF END DATE IS A VALID DATE, CONVERTS TO DATETIME OBJECT
    try:
        end_date = datetime(year, month, day)
    except:
        raise Exception("End date is in the wrong format or is invalid.")
    return end_date


# Chromeのドライバを得る
def open_chrome():
    browser = webdriver.Chrome(executable_path='/Users/akr712/Desktop/Scraping_DataBase_Medium/chromedriver.exe')
    # 暗黙的な待機を最大30秒行う(サーバーの負担軽減)
    browser.implicitly_wait(30)
    return browser

def final_url_builder(tag_url, year, month, day):
    # YYYY/MM/DDというフォーマットに合うように一桁の日にちは二桁にする
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    # 投稿年月日ごとにURLを作成する（のちにこれを用いてクロールする）
    url = tag_url + year + "/" + month + "/" + day
    return url


"""「1つの記事ポスト単位」ごとのテキスト取得"""

def post_cards_finder(soup):
    post_cards = soup.find_all("div", class_="streamItem streamItem--postPreview js-streamItem")
    return post_cards


"""「記事タイトル」のテキスト取得"""

def titles_finder(post_cards):
    # タイトルを正規表現を利用して整形する
    def title_cleaner(title):
        # Mediumのエンコード記号を削除する
        title = title.replace("\xa0"," ")
        title = title.replace("\u200a","")
        title = title.replace("\ufe0f","")
        # 絵文字があれば削除する
        title = re.sub(r'[^\x00-\x7F]+','', title)
        return title

    titles = []
    for post_card in post_cards:
        # タイトルのHTMLタグのクラスは７種類ある
        pattern1 = post_card.find("h3", class_="graf graf--h3 graf-after--figure graf--title")
        pattern2 = post_card.find("h3", class_="graf graf--h3 graf-after--figure graf--trailing graf--title")
        pattern3 = post_card.find("h4", class_="graf graf--h4 graf--leading")
        pattern4 = post_card.find("h3", class_="graf graf--h3 graf--leading graf--title")
        pattern5 = post_card.find("p", class_="graf graf--p graf--leading")
        pattern6 = post_card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf--leading graf--title")
        pattern7= post_card.find("h3", class_="graf graf--h3 graf--startsWithDoubleQuote graf-after--figure graf--trailing graf--title")
        # 各投稿のタイトルはどれかにマッチする
        patterns = [pattern1, pattern2, pattern3, pattern4, pattern5, pattern6, pattern7]
        # タイトルが格納されているかを知らせるチェッカー
        saved = False
        # 最初にマッチしたタイトルを保存する
        for pattern in patterns:
            # 値が入っているかつまだ保存されているタイトルがなければタイトルとして保存
            if ((pattern is not None) and (not saved)):
                title = pattern.text
                title = title_cleaner(title)
                titles.append(title)
                saved = True
        # ループ後もしタイトルが格納されていなければ「タイトルなし」とする
        if not saved:
            titles.append("NaN")

    return titles


"""「ライター名」と「発行主体名」のテキスト取得"""

def authors_and_publications_finder(post_cards):
    authors = []
    publications = []
    for post_card in post_cards:
        # soup.find("タグ名", プロパティ_="プロパティ名")
        author = post_card.find("a", class_="ds-link ds-link--styleSubtle link link--darken link--accent u-accentColor--textNormal u-accentColor--textDarken")
        publication = post_card.find("a", class_="ds-link ds-link--styleSubtle link--darken link--accent u-accentColor--textNormal")

        if author is not None:
            author = author.text
            # 小文字に統一, 絵文字を消す
            author = re.sub("\s+[^A-Za-z]","", author)
            author = re.sub(r"[^\x00-\x7F]+"," ", author)
            authors.append(author)

        else:
            authors.append("NaN")

        if publication is not None:
            publication = publication.text
            publication = re.sub("\s+[^A-Za-z]","", publication)
            publication = re.sub(r"[^\x00-\x7F]+"," ", publication)
            publications.append(publication)

        else:
            publications.append("NaN")

    return authors, publications


"""「投稿日」と「タグ」のテキスト取得"""

def dates_and_tags_finder(tag, year, month, day, post_cards):
    tags = []
    Year = []
    Month = []
    Day = []

    for post_card in post_cards:
        tags.append(tag)
        Year.append(year)
        Month.append(month)
        Day.append(day)
    return tags, Year, Month, Day


"""「読了時間」のテキスト取得"""

def readtime_finder(post_cards):
    reading_times = []
    for post_card in post_cards:

        reading_time = post_card.find("span", class_="readingTime")
        if reading_time is not None:
            # <span class="readingTime" title="27 min read"></span>
            reading_time = reading_time["title"]
            reading_time = reading_time.replace(" min read", "")
            reading_times.append(reading_time)
        else:
            reading_times.append("NaN")

    return reading_times


"""「いいね数（拍手数）」のテキスト取得"""

def claps_finder(post_cards):
    claps = []
    for post_card in post_cards:
        clap = post_card.find("button", class_="button button--chromeless u-baseColor--buttonNormal js-multirecommendCountButton u-disablePointerEvents")
        if clap is not None:
            claps.append(clap.text)
        else:
            claps.append("0")

    return claps


"""「対象記事のURL」を取得"""

def article_link_finder(post_cards):
    links = []
    for post_card in post_cards:
        # <a class href="https://medium.com/dunder-data/minimally-sufficient-pandas-a8e67f2a2428?source=---------0---------------------" ... ...</a>
        link = post_card.find("a", class_="")
        if link is not None:
            links.append(link["href"])
        else:
            raise Exception("cannot find a link")
    return links

"""記事をスクレイピングしていく"""

def scrape_tag(tag, yearstart, monthstart, yearstop, monthstop):

    path = os.getcwd()
    path = path + "/medium_" + tag + ".csv"
    #3. TRY TO OPEN FILE PATH
    try:
        file = open(path, "w")
        file.close()
    except:
        raise Exception("Could not open file.")

    #4. MAKE SURE START DATE <= STOP DATE
    current_date = get_start_date(int(yearstart), int(monthstart), 1)
    end_date = get_start_date(int(yearstop), int(monthstop), 1)
    if current_date > end_date:
        raise Exception("End date exceeds start date.")
    else:
        None

#-------Start Scraping!---------------------------------------------------------------

    # タグごと（"Machine Learning", "AI" etc..）のURLを作る
    base_url = tag_url_builder(tag)
    # Mediumのサーバーはコマンドラインからのリクエストを拒否するため、ブラウジングが必要
    chrome_driver = open_chrome()

    firstPage = True
    counter = 0

    while(current_date <= end_date):
        # 対象のタグに対して、アーカイブされた年月日順にクロールしていく
        url = final_url_builder(base_url, str(current_date.year), str(current_date.month), str(current_date.day))
        response = chrome_driver.get(url)
        soup = BeautifulSoup(chrome_driver.page_source, features="lxml")
        post_cards = post_cards_finder(soup)

        # 記事カード内の各データを取得していく
        titles = titles_finder(post_cards)
        authors, publications = authors_and_publications_finder(post_cards)
        tags, year, month, day = dates_and_tags_finder(tag, current_date.year, current_date.month, current_date.day, post_cards)
        reading_times = readtime_finder(post_cards)
        claps = claps_finder(post_cards)
        links = article_link_finder(post_cards)

        dict = {"Title":titles, "Author":authors, "Publication":publications, "Tag":tags, "Year":year, "Month":month, "Day":day, "Reading_Time":reading_times, "Claps":claps, "link":links}

        vals = list(dict.values())
        for col in vals:
            if len(col)==len(post_cards):
                continue
            else:
                raise Exception("Data length does not match with number of stories on page.")

        df = pd.DataFrame.from_dict(dict)

        if firstPage:
            with open(path, "a") as f:
                df.to_csv(f, mode="a", header=False, index=True)
            firstPage = False

        else:
            with open(path, "a") as f:
                df.to_csv(f, mode="a", header=False, index=True)
        # URLを移動するために、現在の日付の次の日に変える
        current_date = current_date + timedelta(days=1)
        # スクレイプした記事数をカウントしていく
        counter = counter + len(post_cards)
        print(counter, "    ",current_date)
        time.sleep(2)
    chrome_driver.close()
