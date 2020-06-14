import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.dbsparta

# DB에 저장할 영화인들의 출처 url을 가져옵니다.
def get_urls(lecture):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

    url = 'https://hobby.conects.com/lecture/search?q='

    value = lecture

    data = requests.get(url + value, headers=headers)
   
    soup = BeautifulSoup(data.text, 'html.parser')

    trs = soup.select('.hobbyList > .detailWrap > .listTit').text

    urls = []
    for tr in trs:
        a = tr.select_one('.hobbyList > li > a')
        if a is not None:
            baseurl = 'https://hobby.conects.com/'
            url = baseurl + a['href']
            urls.append(url)

    return urls

# 출처 url로부터 영화인들의 사진, 이름, 최근작 정보를 가져오고 mystar 콜렉션에 저장합니다.
def insert_lecture(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    lecture = soup.select_one('.content > div.cont_box > div.classTit > h4').text
    img_url = soup.select_one('.content > div.right > div.movie > div.movieImg > img')['src']
    teacher = soup.select_one(
        '#content > div.article > div.mv_info_area > div.mv_info.character > dl > dd > a:nth-child(1)').text
    price = soup.select_one('.content > div.payBox > div.totalPay > #total_price')
    
    doc = {
        'lecture': lecture,
        'img_url': img_url,
        'teacher': teacher,
        'price': price,
        'url': url
    }

    db.mylecture.insert_one(doc)
    print('완료!', lecture)

# 기존 mystar 콜렉션을 삭제하고, 출처 url들을 가져온 후, 크롤링하여 DB에 저장합니다.
def insert_all():
    db.mylecture.drop()  # mystar 콜렉션을 모두 지워줍니다.
    urls = get_urls()
    for url in urls:
        insert_lecture(url)


### 실행하기
insert_all()
