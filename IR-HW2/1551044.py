#################### Homework2
# Web crawler for vnexpress.net
# Return [title, url, shortcontent]
# Python 3.6.5
# BeautifulSoup 4

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from collections import defaultdict

page_url = 'https://vnexpress.net/'
output_dir = 'articles.txt'

# utility func
def printlist(a):
    for item in a:
        print(item)

def write_file_from_list(ulist):
    with open(output_dir, 'w', encoding='utf-8') as file:
        for article in ulist:
            file.write(str(article))
            file.write('\n')

def format_bad_link(ulist):
    for i in range(len(ulist)):
        if ulist[i].startswith('//'):
            ulist[i] = 'https:' + ulist[i]
        elif 'https://' not in ulist[i]:
            ulist[i] = page_url[:-1] + ulist[i]

    return ulist
            
##### Get all main sections' urls
# 
#
def get_section_urls(page_url):
    try:
        mainpage = urlopen(page_url)
    except HTTPError as err:
        print(err.args)
    except URLError as urlerr:
        print(urlerr.args)

    bs = BeautifulSoup(mainpage, 'html.parser')

    navbar_content = bs.body.find_all(class_='p_menu')
    sections_urls = navbar_content[0].find_all('a')
    print (' --> Processing %d main sections' % (len(sections_urls) - 1))

    sections_list = []

    # Skip first two sections (null & video)
    for i in range(2, len(sections_urls)):
        # Retrieve urls only
        sections_list.append(sections_urls[i].get('href'))

    section_list = format_bad_link(sections_list)
    # printlist(section_list)
    return sections_list



##### For featured articles
# Articles in <article> tag
# With short description
def get_features_articles(section_urls):
    
    retrieved_list = []
    for page_url in section_urls:
        html = urlopen(page_url)

        bs = BeautifulSoup(html, 'html.parser')

        urls = bs.body.find_all('article')
        print(" --> Retrieved %d articles." % len(urls))

        if len(urls) == 0:
            continue

        tmp = []
        
        for i in range(len(urls)):
            title, href, content = '', '', ''
            article = urls[i]
            # print(article)
            try:
                if article.find(class_='title_news') is not None:
                    title = article.find(class_='title_news').find('a').get('title')
                    href = article.find(class_='title_news').find('a').get('href')

                if article.find(class_='description') is not None:
                    content = article.find(class_='description').text
            except:
                pass

            if title == '' and href == '' and content == '':
                continue
            tmp = [title, href, content]
            retrieved_list.append(tmp)
    return retrieved_list

##### Driver function
# VNExpress.net crawler
def vnexpress_crawler(page_url):
    section_urls = get_section_urls(page_url)
    retrieved_list = get_features_articles(section_urls)

    # Write to file
    write_file_from_list(retrieved_list)

    # Notify
    print('Successfully write %d entries to file.' % len(retrieved_list))


vnexpress_crawler(page_url)

