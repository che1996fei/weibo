import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq


base_url = 'https://m.weibo.cn/api/container/getIndex?'
headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/2779895470',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
}


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
            id = item.get('id')
            text = pq(item.get('text')).text()
            image = item.get('bmiddle_pic')
            attitudes = item.get('attitudes_count')
            comments = item.get('attitudes_count')
            reposts = item.get('reposts_count')
            file = open(r'C://Users//Administrator//Desktop//weibo.txt', 'a', encoding='utf-8')
            file.write("id:"+str(id)+'\n'+"微博内容："+text+'\n'+"点赞数："+str(attitudes)+'\n'+"评论数："+str(comments)+'\n'+"转发数："+str(reposts)+'\n')
            file.write('\n' + '=' * 50 + '\n')
            file.close()





if __name__ == '__main__':
    for page in range(1, 48):
        json = get_page(page)
        results = parse_page(json)