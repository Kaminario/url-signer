# -*- coding: utf-8 -*-

import hashlib
import hmac
import json
import time
from urllib.parse import parse_qs, parse_qsl, unquote, urlencode, urlsplit, urlunsplit

import baseconv

__all__ = ("sign", "sign_url", "verify_url")

# A good way to generate key is:
# python -c 'import secrets as s, baseconv as b; print(b.base62.encode(int.from_bytes(s.token_bytes(64), "big")))'

default_valid_for = 600


def sign(key: str, **kwargs):
    msg = json.dumps(kwargs, sort_keys=True)
    mac = hmac.digest(key.encode(), msg.encode(), hashlib.blake2b)
    mac_encoded = baseconv.base62.encode(int.from_bytes(mac, "big"))
    return mac_encoded


def sign_url(key: str, url: str, valid_for_sec: int = default_valid_for):
    url = unquote(url)
    o = urlsplit(url)

    # validate no reserved params
    query = parse_qs(o.query)
    assert "expire" not in query
    assert "signature" not in query

    expire = int(time.time() + valid_for_sec)

    mac_encoded = sign(key, p=o.path, q=query, e=expire)

    # parse query_string to list to preserve the order
    query = parse_qsl(o.query)
    query += (("expire", expire), ("signature", mac_encoded))
    parts = list(o)
    parts[3] = urlencode(query)
    return urlunsplit(parts)


def verify_url(key: str, url: str):
    url = unquote(url)
    o = urlsplit(url)

    try:
        # validate no reserved params
        query = parse_qs(o.query)
        assert "expire" in query
        assert "signature" in query

        expire = int(query.pop("expire")[0])
        assert expire > time.time()

        signature = query.pop("signature")[0]

        mac_encoded = sign(key, p=o.path, q=query, e=expire)

        return mac_encoded == signature
    except Exception:
        return False
