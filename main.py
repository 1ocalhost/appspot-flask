import requests
from flask import Flask, request
from feed import filter_feed_by_words

app = Flask(__name__)


@app.route('/')
def root():
    return 'it works!'


@app.route('/filter_feed')
def filter_feed():
    url = request.args.get('url')
    words = request.args.get('words')
    words = list(filter(bool, words.split(',')))
    resp = requests.get(url)
    return filter_feed_by_words(resp.text, words)


@app.route('/get_content')
def get_content():
    url = request.args.get('url')
    resp = requests.get(url, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
