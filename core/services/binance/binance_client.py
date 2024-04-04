import os
from typing import Dict

from binance import Client


class BinanceClient(Client):
    def _create_website_api_uri(self, path: str, version: int, signed: bool = True) -> str:
        url = self.WEBSITE_URL
        return url + '/' + '/bapi/accounts/v1/private/account/user-config/get'

    def _request_margin_api2(self, method, path, signed=False, version=1, **kwargs) -> Dict:
        uri = self._create_margin_api_uri(path, version)
        uri2 = self._create_website_api_uri(path, version)
        return self._request(method, uri2, signed, **kwargs)

    # def _request_margin_api(self, method, path, signed=False, version=1, **kwargs) -> Dict:
    #     uri = self._create_margin_api_uri(path, version)
    #     return self._request(method, uri, signed, **kwargs)

    # def get_asset_history(self, **data):
    #     uri = self._create_website_api_uri('aaaaaaaaaaaaaaa', self.PUBLIC_API_VERSION)
    #     return self._request('get', uri, True, **data)

    def get_asset_history(self, **params):
        aaa = self._request_margin_api2('get', 'asset/assetDetail', True, data=params)
        return aaa
