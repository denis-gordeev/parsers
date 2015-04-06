import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
month = '01'
year = '2015'
result = ''
driver = webdriver.Firefox()
for day in ('22',):
    driver.get('http://m.lenta.ru/'+year+'/'+month+'/'+day)
    wait = ui.WebDriverWait(driver,5)
    news = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
    links = re.findall(year+'/'+month+'/'+day+'/\w+/',news)
    for link in links:
        print link
        driver.get('http://m.lenta.ru/comments/news/'+link)
        wait = ui.WebDriverWait(driver,5)
        text = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
        posts = re.findall('(<div class="hc_text e_hc_text".*?>)(.*?)(</div>)',text)
        for post in posts:
            if  len(post)<2:
                continue
            print post
            post = re.sub('>>\d+', '', post[1])
            post = re.sub('<span class="unkfunc">&gt;','',post)
            post = re.sub('<br>',' ',post)
            post = re.sub('\n',' ',post)
            post = re.sub('<[/]?strong>','\n',post)
            post = re.sub('<[/]?span.*?>','\n',post)
            post = re.sub('&quot;','"',post)
            post = re.sub('&quot;?','"',post)
            post = re.sub('&#47;','/',post)
            post = '<message link='+link+'>'+post.strip()+'</message>\n'
            result += post 
f = open('comments','w')
f.write(result.encode('utf-8'))
f.close()
