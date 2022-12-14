# https://docs-blockchain.line.biz/api-guide/Authentication#python-sample

import hmac
import hashlib
import base64
from sdk.request_flattener import RequestBodyFlattener


class SignatureGenerator:

    def __createSignTarget(self, method, path, timestamp, nonce, parameters: dict = {}):
        signTarget = f'{nonce}{str(timestamp)}{method}{path}'
        if (len(parameters) > 0):
            signTarget = signTarget + "?"

        return signTarget

    def generate(self, secret: str, method: str, path: str, timestamp: int, nonce: str, query_params: dict = {},
                 body: dict = {}):
        body_flattener = RequestBodyFlattener()
        all_parameters = {}
        all_parameters.update(query_params)
        all_parameters.update(body)

        # self.__logger.debug("query_params: " + str(query_params))

        signTarget = self.__createSignTarget(method.upper(), path, timestamp, nonce, all_parameters)

        if (len(query_params) > 0):
            signTarget += '&'.join('%s=%s' % (key, value) for (key, value) in query_params.items())

        if (len(body) > 0):
            if (len(query_params) > 0):
                signTarget += "&" + body_flattener.flatten(body)
            else:
                signTarget += body_flattener.flatten(body)

        raw_hmac = hmac.new(bytes(secret, 'utf-8'), bytes(signTarget, 'utf-8'), hashlib.sha512)
        result = base64.b64encode(raw_hmac.digest()).decode('utf-8')

        return result
