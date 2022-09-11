from typing import Optional
import logging
from os import environ

from BlockChainWrapper import BlockChainWrapper

logging.basicConfig(format="[%(levelname)s] %(asctime)s %(message)s", level=logging.DEBUG)


class MyBlockChain(BlockChainWrapper):
    """
    Sample class using `BlockChainWrapper`

    Use `self.request(...)` to make your request with signature
    """

    def __init__(self, api_key, api_secret, wallet_address, wallet_secret):
        super().__init__(api_key, api_secret, wallet_address, wallet_secret)

    def get_wallets(self) -> dict:
        """
        GET example
        https://docs-blockchain.line.biz/api-guide/category-service-wallets/retrieve#v1-wallets-get
        """
        method = 'GET'
        path = '/v1/wallets'
        return self.request(method, path)

    def mint_nft(self, contract_id: str, token_type: str, name: str, to_address: str, meta: Optional[str]) -> dict:
        """
        POST example
        https://docs-blockchain.line.biz/api-guide/category-item-tokens/mint-burn#v1-item-tokens-contractId-non-fungibles-tokenType-mint-post
        """
        method = 'POST'
        path = f'/v1/item-tokens/{contract_id}/non-fungibles/{token_type}/mint'
        body = {
            "ownerAddress": self.wallet_address,
            "ownerSecret": self.wallet_secret,
            "toAddress": to_address,
            "name": name,
        }
        if meta:
            body["meta"] = meta
        return self.request(method, path, request_body=body)


def main():
    bc = MyBlockChain(
        api_key=environ.get('API_KEY'),
        api_secret=environ.get('API_SECRET'),
        wallet_secret=environ.get('WALLET_SECRET'),
        wallet_address=environ.get('WALLET_ADDRESS'),
    )
    bc.get_wallets()

    # bc.mint_nft(environ.get('CONTRACT_ID'), '10000001', 'MyAwesomeNFT', bc.wallet_address, '{"hello":"world"}')
    pass


if __name__ == '__main__':
    main()
