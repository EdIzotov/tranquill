class FinanceService:
    @staticmethod
    def calculate_avg_price(history, asset, current_price):
        avg_data = {}

        total_price = 0
        total_volume = 0
        avg_price = 0
        profit = 0

        for h in history:
            if h.side == 'BUY':
                if float(h.price) > 0:
                    total_price = total_price + float(h.price) * float(h.executedQty)
                else:
                    total_price = total_price + float(h.cummulativeQuoteQty)
                total_volume = total_volume + float(h.executedQty)
                avg_price = total_price / total_volume
            elif h.side == 'SELL':
                total_price = total_price - avg_price * float(h.executedQty)
                total_volume = total_volume - float(h.executedQty)
                profit = profit + ((float(h.price) - float(avg_price)) * float(h.executedQty))

        pnl = (float(current_price) - float(avg_price)) * 100 / float(current_price)
        avg_data['asset'] = asset
        # if total_price >= 0:
        #     avg_data['total_price'] = total_price
        #     avg_data['profit'] = 0
        # else:
        #     avg_data['total_price'] = 0
        #     avg_data['profit'] = total_price * -1
        avg_data['total_volume'] = total_volume
        avg_data['avg_price'] = avg_price
        avg_data['pnl'] = pnl
        avg_data['profit'] = profit
        return avg_data

    @staticmethod
    def get_amount_in_usdt(amount, price):
        return amount * price
