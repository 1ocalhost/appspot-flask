import json
import base64


def b64_decode(data):
    if data is None:
        return None

    d = data.replace('_', '/').replace('-', '+')
    return base64.b64decode(d.strip() + '==').decode()


def b64_encode(data):
    if isinstance(data, str):
        data = data.encode()
    return base64.b64encode(data)


def block_to_list(block):
    result = b64_decode(block).split('\n')
    return list(filter(len, result))


def list_to_block(list_):
    list_ = list(list_)
    return b64_encode('\n'.join(list_))


def decode_uri(uri):
    scheme, data = uri.split('://')
    data = b64_decode(data)
    decoder = encoding_provider(scheme)[0]
    return scheme, decoder(data)


def encode_uri(item):
    scheme, obj = item
    encoder = encoding_provider(scheme)[1]
    data = encoder(obj)
    return scheme + '://' + b64_encode(data).decode()


def encoding_provider(scheme):
    return {
        'vmess': [json.loads, json.dumps],
    }.get(scheme)


def filter_feed(feed, filter_):
    servers = block_to_list(feed)
    servers = map(decode_uri, servers)
    servers = [s for s in servers if filter_(s)]
    servers = map(encode_uri, servers)
    return list_to_block(servers)


def filter_feed_by_words(feed, words):
    def filter_(server):
        scheme, obj = server
        if scheme == 'vmess':
            label = obj['ps']

        for word in words:
            if word in label:
                return False
        return True

    return filter_feed(feed, filter_)
