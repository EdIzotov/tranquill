import csv
import os

from binance import Client
from tabulate import tabulate


def read_data_file(file):
    with open(file, mode='r') as data_file:
        trade_data = csv.reader(data_file)
        next(trade_data, None)
        data = []
        for order in trade_data:
            raw_order = {
                'date': order[0],
                'currency_from': order[1],
                'amount_from': order[2],
                'currency_to': order[3],
                'amount_to': order[4]
            }
            data.append(raw_order)
        return data


def calculate_balance(orders_data):
    balance_raw = {}
    pnl = 'pnl'
    avg_price = 'avg_price'
    total_volume = 'total_volume'
    amount_in_usdt = 'amount_in_usdt'
    for o in orders_data:
        currency_from = 'currency_from'
        amount_from = 'amount_from'
        currency_to = 'currency_to'
        amount_to = 'amount_to'
        amount = 'amount'
        total_price = 'total_price'
        profit = 'profit'

        if o[currency_from] not in balance_raw:
            balance_raw[o[currency_from]] = {amount: 0, avg_price: 0, amount_in_usdt: 0, total_price: 0, total_volume: 0, profit: 0, pnl: 0}
        if o[currency_to] not in balance_raw:
            balance_raw[o[currency_to]] = {amount: 0, avg_price: 0, amount_in_usdt: 0, total_price: 0, total_volume: 0, profit: 0, pnl: 0}

        if o[currency_from] == 'USDT':
            balance_raw[o[currency_to]][total_price] = balance_raw[o[currency_to]][total_price] + float(o[amount_from])
            balance_raw[o[currency_to]][total_volume] = balance_raw[o[currency_to]][total_volume] + float(o[amount_to])
            balance_raw[o[currency_to]][avg_price] = balance_raw[o[currency_to]][total_price] / balance_raw[o[currency_to]][total_volume]
        else:
            balance_raw[o[currency_from]][total_price] = balance_raw[o[currency_from]][total_price] - balance_raw[o[currency_from]][avg_price] * float(o[amount_from])
            balance_raw[o[currency_from]][total_volume] = balance_raw[o[currency_from]][total_volume] - float(o[amount_from])
            balance_raw[o[currency_from]][profit] = (float(o[amount_to]) / float(o[amount_from]) - float(balance_raw[o[currency_from]][avg_price])) * float(o[amount_from])

    for key in balance_raw.keys():
        base_currency = 'USDT'
        if key != 'USDT':
            binance = Client('', '')
            current_price = binance.get_avg_price(symbol=key + base_currency)['price']
            balance_raw[key]['current_price'] = float(current_price)
            if balance_raw[key][total_volume] * balance_raw[key]['current_price'] < 1:
                balance_raw[key][pnl] = float(0)
            else:
                balance_raw[key][pnl] = (float(current_price) - balance_raw[key][avg_price]) * 100 / balance_raw[key][avg_price]
            balance_raw[key][amount_in_usdt] = balance_raw[key][total_volume] * balance_raw[key][avg_price]
        else:
            balance_raw[key]['current_price'] = float(1)
            balance_raw[key][pnl] = float(0)
    return balance_raw


def print_balance(balance_data):
    data_to_print = []
    profit_total = 0
    position_total = 0
    position_to_close = 0
    for asset in balance_data:
        if balance_data[asset]['total_volume'] > 0 or balance_data[asset]['profit'] > 0:
            data_to_print.append([asset, str("%.8f" % float(balance_data[asset]['total_volume'])),
                                  balance_data[asset]['amount_in_usdt'],
                                  balance_data[asset]['avg_price'],
                                  balance_data[asset]['current_price'], balance_data[asset]['pnl'],
                                  balance_data[asset]['profit']])
        profit_total = profit_total + balance_data[asset]['profit']
        position_total = position_total + balance_data[asset]['amount_in_usdt']
        position_to_close = position_to_close + balance_data[asset]['total_volume'] * balance_data[asset]['current_price']
    print(tabulate(data_to_print, headers=['Asset', 'Amount', 'Amount in USDT', 'Avg_Price', 'Current_Price', 'PNL (%)', 'Profit']))
    print('===========================================================================================================')
    print('Profit total:\t\t' + str(profit_total))
    print('Position total:\t\t' + str(position_total))
    print('Close position:\t\t' + str(position_to_close))
    print('Close - Total:\t\t' + str(position_to_close - position_total))
    print('Total year:\t\t' + str(position_to_close - position_total + profit_total))


def get_data_file():
    files = os.listdir('.')
    for file in files:
        if file.lower().endswith('.csv'):
            return file


data_file = get_data_file()
if data_file is None:
    print('No data file was found. Place a CSV file in the root of the directory.')
else:
    orders = read_data_file(data_file)
    balance = calculate_balance(orders)
    print_balance(balance)
