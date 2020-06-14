from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta


# HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')

# API 역할을 하는 부분
@app.route('/api/list', methods=['GET'])
def lecture_list():
    # 1. mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    # 참고- find({},{'_id':False}), sort()를 활용하면 굿!
    lecture = list(db.mylecture.find({},{'_id':False}).sort('like',-1))
    # flask에서 제공하는 sort() 정렬하는 함수 -1 desc 내림차순 / 1 asc 오름차순
    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success','msg':'list 연결되었습니다!','lecture':lecture})

@app.route('/api/searching', methods=['POST'])
def star_like():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    keyword_receive = request.form['keyword_give']
    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    lecture = db.mylecture.find_one({'lecture':lecture_receive})
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = lecture['like'] + 1
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    db.mystar.update({'lecture':lecture_receive},{'$set':{'like':new_like}})
    # update ({조건},{'$set':{바꿀것}})
    
    # 참고: '$set' 활용하기!
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','msg':'like 연결되었습니다!'})


@app.route('/api/delete', methods=['POST'])
def star_delete():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    lecture_receive = request.form['lecture_give']
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.mystar.delete_one({'lecture':lecture_receive})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success','msg':'delete 연결되었습니다!'})

    

if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)