import requests
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def root():
    return 'it works!'


@app.route('/get_content')
def get_content():
    url = request.args.get('url')
    resp = requests.get(url, stream=True)
    return resp.raw.read(), resp.status_code, resp.headers.items()


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
