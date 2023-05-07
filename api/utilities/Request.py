import certifi
import urllib3

from PostgresStorage import PostgresStorage


class Request:
    storage: PostgresStorage

    def get_headers(self) -> dict:
        return {'X-Auth-Token': self.storage.get_api_key(), 'Host': self.storage.get_base_url()}

    def make_api_call(self, url: str, method: str):
        pool_manager = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        return pool_manager.request(method=method, url=url, headers=self.get_headers())

    def __init__(self, storage: PostgresStorage):
        self.storage = storage
