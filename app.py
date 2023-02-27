from flask import Flask, render_template, request
from flask_paginate import Pagination, get_page_parameter
import requests

app = Flask(__name__)

# ホットペッパーグルメサーチAPIのエンドポイント
HOTPEPPER_API_ENDPOINT = 'https://webservice.recruit.co.jp/hotpepper/gourmet/v1/'

# ホットペッパーグルメサーチAPIのアクセスキー
HOTPEPPER_API_ACCESS_KEY = "APIキー"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods = ['POST'])
def search():
    # フォームから送信された現在地の緯度・経度を取得
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    selectedRange = request.form.get('selran')

    # ホットペッパーグルメサーチAPIにリクエストを送信
    params = {
        'key': HOTPEPPER_API_ACCESS_KEY,
        'lat': latitude,
        'lng': longitude,
        'range': selectedRange, # 検索範囲
        'format': 'json', # レスポンスの形式
    }
    response = requests.get(HOTPEPPER_API_ENDPOINT, params=params)

    # レスポンスをJSON形式で取得
    data = response.json()

    # レストランのリストを取得
    restaurants = data['results']['shop']
    
    #ページネーション
    page = request.args.get(get_page_parameter(),type = int, default = 1)
    per_page = 5
    pagination = Pagination(page = page, total = len(restaurants), per_page = per_page, css_framework = 'bootstrap4')
    
    start = (page - 1) * per_page
    end = start + per_page
    page_restaurants = restaurants[start: end]
    
    context = {
        'restaurants': page_restaurants,
        'pagination': pagination,
    }

    # 検索結果をテンプレートに渡して表示
    return render_template('search.html', **context)
@app.route('/restaurant/<string:restaurant_id>')
def restaurant_detail(restaurant_id):
    params = {
        'key': HOTPEPPER_API_ACCESS_KEY,
        'id': restaurant_id,
        'format': 'json',
    }
    response = requests.get(HOTPEPPER_API_ENDPOINT, params = params)
    #レスポンスをjson形式で取得
    data = response.json()
    #受け取ったリストから選択されたお店を取得
    shop = data['results']['shop'][0]
    return render_template('detail.html', shop = shop)    

if __name__ == "__main__":
    app.run(debug = True)