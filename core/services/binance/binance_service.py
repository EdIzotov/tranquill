import os
import time

from core.models.asset_history import AssetHistoryRow
from core.services.binance.binance_client import BinanceClient
from core.services.date.date_service import DateService
from core.services.finance.finance_service import FinanceService


class BinanceService:
    def __init__(self):
        env = os.environ
        self.api_key = os.environ.get('binance_api_key')
        self.secret_key = os.environ.get('binance_secret_key')
        self.client = BinanceClient(self.api_key, self.secret_key)

    def get_assets(self):
        ignore_currencies = ['UAH', 'LDONE']
        assets_raw = self.client.get_account()['balances']
        assets = []
        index_counter = 0
        for asset_raw in assets_raw:
            if float(asset_raw['free']) > 0 or float(asset_raw['locked']) > 0:
                if asset_raw['asset'] in ignore_currencies:
                    continue
                if asset_raw['asset'] == 'USDT':
                    asset = {
                        'index': index_counter,
                        'asset': asset_raw['asset'],
                        'place': 'end',
                        'text': asset_raw['asset'],
                        'values': (
                            str("%.8f" % float(asset_raw['free'])),
                            str("%.8f" % float(asset_raw['locked'])),
                            float(asset_raw['free']) + float(asset_raw['locked']),
                            '1',
                            '1',
                            '0'
                        )
                    }

                    index_counter = index_counter + 1
                    assets.append(asset)
                    continue

                history = self.get_asset_history(asset_raw['asset'], 'USDT')
                pair = asset_raw['asset'] + 'USDT'
                current_price = self.client.get_avg_price(symbol=pair)['price']
                avg_data = FinanceService.calculate_avg_price(history, asset_raw['asset'], current_price)

                amount_in_usdt = FinanceService.get_amount_in_usdt(float(asset_raw['free']) + float(asset_raw['locked']), float(current_price))

                asset = {
                    'index': index_counter,
                    'asset': asset_raw['asset'],
                    'place': 'end',
                    'text': asset_raw['asset'],
                    'values': (
                        str("%.8f" % float(asset_raw['free'])),
                        str("%.8f" % float(asset_raw['locked'])),
                        str("%.8f" % amount_in_usdt),
                        str("%.8f" % avg_data['avg_price']),
                        current_price,
                        str("%.2f" % avg_data['pnl']),
                        str("%.2f" % avg_data['profit'])
                    )
                }

                index_counter = index_counter + 1
                if amount_in_usdt > 1:
                    assets.append(asset)
        return assets

    def get_asset_history(self, pair_to, pair_from, start=None, end=None):
        history = []
        if pair_to == pair_from:
            return history

        current_time = int(round(time.time() * 1000))
        start_time = current_time - (24 * 60 * 60 * 1000)

        data = self.client.get_all_orders(symbol=pair_to + pair_from)
        data_filled = []
        for d in data:
            if d['status'] == 'FILLED':
                data_filled.append(d)
        for d in data_filled:
            asset_dto = AssetHistoryRow(**d)
            history.append(asset_dto)
        return history
