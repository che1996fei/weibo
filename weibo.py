import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2779895470',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}

def get_page():
    params = {
        'type': 'uid',
        'value': '2779895470',
        'containerid': '1076032779895470',
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




if __name__ == '__main__':
    json = get_page()
    results = parse_page(json)
    for result in results:
        print(result)





