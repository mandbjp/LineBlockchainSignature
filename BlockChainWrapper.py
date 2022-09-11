import string
import random
import time
import logging
from typing import Optional
from pprint import pformat

import requests


from sdk.signature_generator import SignatureGenerator

# Cashew
SERVER_URL = 'https://test-api.blockchain.line.me'


class BlockChainWrapper:
    api_key: str
    api_secret: str
    wallet_address: str
    wallet_secret: str

    def __init__(self, api_key: str, api_secret: str, wallet_address: str, wallet_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.wallet_secret = wallet_secret
        self.wallet_address = wallet_address
        self.logger = logging.getLogger(__name__)

    def get_nonce_timestamp_headers(self, content_type='application/json'):
        nonce = ''.join(
            random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(8))
        timestamp = int(round(time.time() * 1000))
        headers = {
            'service-api-key': self.api_key,
            'nonce': nonce,
            'timestamp': str(timestamp),
        }
        if content_type != '':
            headers['Content-Type'] = content_type
        return nonce, timestamp, headers

    def request(self, method: str, path: str, query_params: Optional[dict] = None, request_body: Optional[dict] = None):
        if method not in ['GET', 'POST', 'PUT']:
            raise ValueError('invalid method')
        query_params = query_params or {}
        request_body = request_body or {}

        nonce, timestamp, headers = self.get_nonce_timestamp_headers()

        signature = SignatureGenerator().generate(self.api_secret, method, path, timestamp, nonce,
                                                  query_params=query_params, body=request_body)
        headers['signature'] = signature

        self.logger.debug(f'BC-Request: {method} {path}')
        if method == 'GET':
            res = requests.get(SERVER_URL + path, headers=headers, params=query_params)
        else:
            res = requests.post(SERVER_URL + path, headers=headers, params=query_params, json=request_body)

        ret = res.json()
        self.logger.debug(f'BC-Response: {res.status_code}\n{pformat(ret)}')
        return ret
