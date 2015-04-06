#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import cfscrape
import re
import json
from nltk.tokenize.punkt import PunktWordTokenizer
from openpyxl import load_workbook
import codecs
import os
'''
used https://github.com/Anorov/cloudflare-scrape
used https://github.com/emmetio/pyv8-binaries
'''
class Post():
    def __init__(self, date, text, num, thread_url):
        self.date = date
        self.text = text
        self.num = num
        self.link = thread_url+'#'+self.num
        self.source = re.findall('http[s]?://2ch.hk/.*?/',thread_url,re.DOTALL)[0]
        self.title = ''
        self.markers = ''
        self.tone = 0
        self.emotion = 'neutral'
threads_url = "http://2ch.hk/po/res/" #change

def parse_post(post, thread_url):
    post_html = post[1]
    date = re.findall('(<span class="posttime">)(.*?)(&nbsp;</span>)',post_html, re.DOTALL)[0][1]
    text = re.findall('(<blockquote.*?>)(.*?)(</blockquote>)',post_html, re.DOTALL)[0][1]
    cite = re.findall('>>>\d+', text)
    if cite:
        for el in cite:
                text = re.sub('<a href=.*?>>>\d+</a><br>',el+'\n',text)
    text = re.sub('<span class="unkfunc">&gt;','',text)
    text = re.sub('<br>',' ',text)
    text = re.sub('\n',' ',text)
    text = re.sub('<[/]?strong>','\n',text)
    text = re.sub('<[/]?span.*?>','\n',text)
    text = re.sub('&quot;','"',text)
    text = re.sub('&quot;?','"',text)
    text = re.sub('&#47;','/',text)
    title = re.findall('(<span class="post-title">)(.*?)(</span>)',post_html, re.DOTALL)
    if title:
        title = title[0][1]
    else:
        title = ''
    post_num = re.findall('(data-num=")(\d+)',post_html, re.DOTALL)[0][1]
    post = Post(date,text,post_num, thread_url)
    if title:
        post.title = title
    #print post.link
    #print post.text
    return post

def download (link):
    scraper = cfscrape.create_scraper() # returns a requests.Session object
    text = scraper.get(link).text # => "<!DOCTYPE html><html><head>..."
    threads = re.findall('thread-\d+',text)
    for thread in threads:
        thread = thread[7:] #remove the word thread-
        print(threads_url+thread+".html")
        url = threads_url+thread+".html"
        thread_text = scraper.get(url).text
        parse_thread(thread_text, url, thread)

def save_thread(thread_txt, thread_num):
    thread_file = open('2ch-po'+os.sep+thread_num+'.txt', 'w+') #change
    thread_file.write(thread_txt.encode('utf-8'))
    thread_file.close()

def parse_thread(text, thread_url, thread_number):
    post_first = re.findall('(<div class="post oppost".*?data-num="\d+">)(.*?)(<div class="de-refmap">)',text, re.DOTALL) #1st post
    posts = re.findall('(<div id="post-\d+" class="post-wrapper">)(.*?)(<div id="post-\d+" class="post-wrapper">)',text, re.DOTALL)
    posts = post_first + posts
    thread_html = text
    all_posts = {}
    added_posts = []
    thread_txt = ''
    for post in posts:
        post = parse_post(post,thread_url)
        if len(post.text)>0:
            thread_txt += '<message number='+post.num+'>'+post.text.strip()+'</message>\n'
    if thread_txt:
        save_thread(thread_txt,thread_number)
#download('http://2-chru.net/bb/')
while 1:
    download("http://2ch.hk/po/") #change
#download("http://2ch.hk/b/")

