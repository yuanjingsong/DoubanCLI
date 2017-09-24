#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Command Line tool to query the movie rate in Douban
    doubanCLI
    ~~~~~~
    Query Movie/Book info in Douban
    :Date  09/20/2017
    :author yuanjingsong
    :license: MIT
    :copyright: Copyright (c) 2017 YuanJingsong. All rights reserved
    Usage:
        douban.py -m <title>
        douban.py -b <title>
        douban.py -H
"""
import requests
import json
from pprint import pprint
from docopt import docopt
import sys

__name__ = "douban-cli"
__version__ = "0.0.1"
__description__ = "命令行下查询豆瓣电影图书信息"
__keywords__ = "Query Movie or Book info in Douban via CLI"
__author__ = "yuanjingsong"
__constact__ = "yuanjingsongxjtu@gmail.com"
__license__ = "MIT"

class Movie():
    Dou_api = "http://api.douban.com/v2/movie/search?q="
    Movie_detail_api = "http://api.douban.com/v2/movie/subject/"
    def __init__(self,argv):
        movie = ''
        if len(argv) > 0 :
            for s in argv:
                movie = movie + s + ""
            self.Dou_api = self.Dou_api + movie
        self.search()
    def search(self):
        try:
            query = requests.get(self.Dou_api).json()
            id = query['subjects'][0]['id']
            movie_detail = requests.get(self.Movie_detail_api + id).json()
            print('\033[1;31m####################################################### \033[0m')
            print("影片:  " + movie_detail["title"] + "\n")
            print("上映:  " + movie_detail['year'] + "\n")
            print("类型:  ",end = "")
            printList(movie_detail['genres'])
            print('\n')
            if(movie_detail.__contains__("duration")):
                print("片长:  " + movie_detail['duration'] + "\n")
            print("豆瓣评分:  " +str(movie_detail['rating']['average']) + "\n")
            searchImbd(movie_detail['original_title'],movie_detail['year'])
            print("简介:  " + movie_detail['summary'])
            print('\033[1;31m###################################################### \033[0m')
        except Exception as e:
            print(e.message)
class Book():
    api = "https://api.douban.com/v2/book/search?q="
    book_detail_api = "https://api.douban.com/v2/book/"
    def __init__(self,argv):
        book = ""
        if len(argv) > 0 :
            for s in argv:
                book = book + s + ""
            self.api = self.api + book
        self.search()
    def search(self):
        try:
            query = requests.get(self.api).json()
            first = query['books'][0]['id']
            self.searchTimes(first)
        except Exception as e:
            print(e)
    def searchTimes(self, times):
        try:
            book_detail = requests.get(self.book_detail_api + times).json()
            print('\033[1;31m####################################################### \033[0m')
            print("书籍:  " + book_detail['title'] + "\n")
            print("作者:  " + book_detail['author'][0] + "\n")
            print("标签:  ",end="")
            printDict(book_detail['tags'])
            print("\n")
            print("出版社:  " + book_detail['publisher'] + "\n")
            # print("出版日期:  " + book_detail['pubdate'] + "\n")
            print("定价:  " + book_detail['price'] + "\n")
            print("豆瓣评分:  " + book_detail['rating']['average'] + "\n")
            print("作者简介:  " + book_detail['author_intro'] + "\n")
            print("概要:  " + book_detail['summary'] + "\n")
            print('\033[1;31m####################################################### \033[0m')
        except Exception as e:
            print(e.message)
def Search_Hot():
    api_url = "http://api.douban.com/v2/movie/in_theaters"
    try:
        hot_detail = requests.get(api_url).json()
        hot_movies = hot_detail['subjects']
        for i in hot_movies:
            printMovie(i)
    except Exception as e:
        print(e)
def printMovie(movie):
    if(str(movie["rating"]["average"]) != "0"):
        print('\033[1;31m####################################################### \033[0m')
        print("影片:  " + movie["title"] + "\n")
        print("评分:  " + str(movie["rating"]["average"]) + "\n")
        try:
            searchImbd(movie['original_title'],movie['year'])
        except Exception as e :
            print("暂无评分\n")
        print("类型:  ",end = "")
        printList(movie['genres'])
        print("\n")
        print("链接:  " + movie['alt'] + "\n")
        print('\033[1;31m####################################################### \033[0m')
        print('\033[1;31m------------------------------------------------------- \033[0m')
def printList(list):
    for index in list:
        print(index,end = " ")
def printDict(dict):
    for i in dict:
        print(i["name"],end = " ")
def searchImbd(title, year):
    Imdb_api = "http://www.theimdbapi.org/api/find/movie"
    Imdb_para = {"title": title, "year": year}
    imdb_detail = requests.get(Imdb_api, params = Imdb_para).json()
    print("Imdb评分:  " + imdb_detail[0]['rating'] + '\n')
def main():
    arguments = docopt(__doc__)
    if(arguments['-m'] is True):
        Movie(arguments['<title>'])
    elif (arguments['-b'] is True):
        Book(arguments['<title>'])
    elif (arguments['-H'] is True):
        Search_Hot()
main()
