import certifi
import urllib3


class Request:
    api_key: str
    base_url: str

    def get_headers(self) -> dict:
        return {'X-Auth-Token': self.api_key, 'Host': self.base_url}

    @staticmethod
    def get_manager() -> urllib3.PoolManager:
        return urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def make_api_call(self, url: str, method: str):
        return self.get_manager().request(method=method, url=url, headers=self.get_headers())

    def pass_profile(self, user_id: int, s_number: int):
        url: str = 'https://%s/pass/%s' % (self.base_url, user_id)
        return self.get_manager().request(method='GET', url=url, headers=self.get_headers(),
                                          fields={'s_number': s_number})

    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
