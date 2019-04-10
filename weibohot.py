import requests
import json
from bs4 import BeautifulSoup

def get_page():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
    data = {'cata': 'realtimehot'}
    try:
        response = requests.get('https://s.weibo.com/top/summary?', params=data, headers=headers)
        if response.status_code == 200:
            html = response.text
            return html
    except:
        print(None)

def parse_page(html):
    soup = BeautifulSoup(html,'lxml')
    


if __name__ == '__main__':
    get_page()