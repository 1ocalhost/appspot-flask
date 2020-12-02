import re
import requests
from urllib.parse import urlencode


def parse_js_var_value(line):
    r = re.search(r"'([^']+)'", line)
    if r:
        return r.group(1)


def parse_vars_from_html(html, vars_):
    html_lines = html.splitlines()
    for var_name, var_value in vars_.items():
        for line in html_lines:
            if var_name in line:
                line_no_blank = line.replace(' ', '')
                if f'var{var_name}=' in line_no_blank:
                    vars_[var_name] = parse_js_var_value(line)


def get_api_url(share_id, folder_id):
    r = requests.get('https://cloud.189.cn/t/' + share_id)
    vars_ = {
        '_shareId': None,
        '_verifyCode': None,
    }

    parse_vars_from_html(r.text, vars_)
    params = {
        'fileId': folder_id,
        'shareId': vars_['_shareId'],
        'verifyCode': vars_['_verifyCode'],
        'orderBy': 1,
        'order': 'ASC',
        'pageNum': 1,
        'pageSize': 60,
    }

    api_base = 'https://cloud.189.cn/v2/listShareDir.action?'
    return api_base + urlencode(params)


def read_json_dl_link(api_url, filename):
    r = requests.get(api_url)
    for item in r.json()['data']:
        if item['isFolder']:
            continue
        if item['fileName'] == filename:
            return 'https:' + item['downloadUrl']


def parse_dl_link(share_id, folder_id, filename):
    api_url = get_api_url(share_id, folder_id)
    dl_link = read_json_dl_link(api_url, filename)
    if not dl_link:
        return

    r = requests.get(dl_link, allow_redirects=False)
    if r.status_code // 100 == 3:
        return r.headers['Location']
