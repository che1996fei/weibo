import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
from pymongo import MongoClient

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2779895470',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

client = MongoClient()
db = client['weibo']
collection = db['weibo']

def get_page(page):
    params = {
        'type': 'uid',
        'value': '2779895470',
        'containerid': '1076032779895470',
        'page': page
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['id'] = item.get('id')
            weibo['内容'] = pq(item.get('text')).text()
            weibo['点赞'] = item.get('attitudes_count')
            weibo['评论'] = item.get('comments_count')
            weibo['转发'] = item.get('reposts_count')
            yield weibo

def save_to_mongo(result):
    if collection.insert_one(result):
        print('Saved to Mongo')


if __name__ == '__main__':
    for page in range(1, 48):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            save_to_mongo(result)
