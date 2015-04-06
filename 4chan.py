#!/usr/bin/python3.2
#save fourchan pages
#from urllib.request import urlopen
#import http.client
#from urllib.parse import urlparse
from re import findall, sub
import re
import time
from bs4 import BeautifulSoup
import cfscrape
import codecs

def save_site():
    def checkUrl(url):
        p = urlparse(url)
        conn = http.client.HTTPConnection(p.netloc)
        conn.request('HEAD', p.path)
        resp = conn.getresponse()
        return resp.status < 400
    def parse_thread(thread):
        soup = BeautifulSoup(thread)
        posts = ''
        bq = soup.find_all('blockquote')
        for el in bq:
            if len(bq) == 0:
                continue
            post = ''.join(el.get_text())
            post = re.sub('>>\d+', '', post)
            post = re.sub('<span class="unkfunc">&gt;','',post)
            post = re.sub('<br>',' ',post)
            post = re.sub('\n',' ',post)
            post = re.sub('<[/]?strong>','\n',post)
            post = re.sub('<[/]?span.*?>','\n',post)
            post = re.sub('&quot;','"',post)
            post = re.sub('&quot;?','"',post)
            post = re.sub('&#47;','/',post)
            post = '<message>'+post.strip()+'</message>\n'
            posts += post 
        return posts
    def write_html(url, site_folder, string_index=0):
        scraper = cfscrape.create_scraper() # returns a requests.Session object
        text = scraper.get(url).text # => "<!DOCTYPE html><html><head>..."
        threads = re.findall('thread/\d+',text)
        threads = set(threads)
        for thread in threads:
            thread_page = scraper.get(url+thread+'.html').text
            print(url+thread+'.html')
            thread_name = re.sub('thread/','',thread)
            thread_text = thread_page
            thread_file = open(site_folder+thread_name+'.txt', 'w+')
            thread_text = parse_thread(thread_text)
            thread_file.write(thread_text.encode('utf-8'))
    write_html("http://boards.4chan.org/pol/", 'threads/')
    time.sleep(180)

while True:
    save_site()
