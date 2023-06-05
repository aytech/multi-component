import certifi
import urllib3

from PostgresStorage import PostgresStorage
from db.dao import UserDao


class Request:
    storage: PostgresStorage

    def get_headers(self) -> dict:
        return {'X-Auth-Token': self.storage.get_api_key(), 'Host': self.storage.get_base_url()}

    @staticmethod
    def get_manager() -> urllib3.PoolManager:
        return urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def make_api_call(self, url: str, method: str):
        return self.get_manager().request(method=method, url=url, headers=self.get_headers())

    def pass_profile(self, user_id: int, s_number: int):
        url: str = 'https://%s/pass/%s' % (self.storage.get_base_url(), user_id)
        return self.get_manager().request(method='GET', url=url, headers=self.get_headers(),
                                          fields={'s_number': s_number})

    def __init__(self, storage: PostgresStorage):
        self.storage = storage
