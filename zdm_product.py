from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import requests
import pymongo


keyword = 'ipad'
MAX_PAGE = 5
MONGO_URL = 'localhost'
MONGO_DB = 'smzdm'
MONGO_COLLECTION = 'products'
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]
#client = pymongo.MongoClient(host='localhost', port=27017)

keyword = 'ipad'

MAX_PAGE = 5

SERVICE_ARGS = ['--load-images=false', '--disk-cache=true']

# it之家获取最新咨询
"""
def getnew_list(page):
    global pages
    base_url = "https://search.smzdm.com/?c=home&s="

    url = base_url + keyword+'&p='+page
    print(url)
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'

    header = {'User-Agent': user_agent}
    r = requests.get(url = url, headers=header)
    r.raise_for_status()
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'lxml')
    #print(soup.find_all("li",{"class":"feed-row-wide "}))

    for data in soup.find_all("li",{"class":"feed-row-wide "}):
        title = data.a['title']
        value = data.find("div",{"class":"z-highlight"}).string
        tag = data.find("div",{"class":"feed-block-descripe"}).text
        date = data.find("span",{"class":"feed-block-extras"}).string

        print(title,value,tag)
"""



def index_page(page):
    """
    抓取索引页
    :param page: 页码
    """

    print('正在爬取第', page, '页')

    if page == 1:
        base_url = "https://search.smzdm.com/?c=home&s="
        url = base_url + keyword
        get_products(url)

    else :
        base_url = "https://search.smzdm.com/?c=home&s="
        url = base_url + keyword  +'&p='+ str(page)
        get_products(url)

    print(url)





def get_products(url):
    """
    提取商品数据
    """

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:58.0) Gecko/20100101 Firefox/58.0'
    header = {'User-Agent': user_agent}
    r = requests.get(url=url, headers=header)
    r.raise_for_status()
    r.encoding = 'utf-8'

    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup.find_all("li",{"class":"feed-row-wide "}))

    for data in soup.find_all("li", {"class": "feed-row-wide "}):
        product = {
            'title' : data.a['title'],
            'value' : data.find("div", {"class": "z-highlight"}).string,
            'tag'   : data.find("div", {"class": "feed-block-descripe"}).text.replace("\n", "").replace(' ', ''),  #去掉换行和空格
            'date'  : data.find("span", {"class": "feed-block-extras"}).text.replace("\n", "").replace(' ', ''),
            'html'  : data.a['href']
        }
        print(product)
        save_to_mongo(product)



def save_to_mongo(result):
    """
    保存至MongoDB
    :param result: 结果
    """

    #client = pymongo.MongoClient(host='localhost', port=27017)

    try:
        if db[MONGO_COLLECTION].insert(result):
            print('存储到MongoDB成功')
    except Exception:
        print('存储到MongoDB失败')


def main():
    """
    遍历每一页
    """
    for i in range(1, MAX_PAGE + 1):
        index_page(i)
    print("爬取结束")


if __name__ == '__main__':
    main()

