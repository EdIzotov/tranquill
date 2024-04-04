from dataclasses import dataclass


@dataclass
class AssetHistoryRow:
    def __init__(self, **data):
        self.symbol = None
        self.orderId = None
        self.orderListId = None
        self.clientOrderId = None
        self.price = None
        self.origQty = None
        self.executedQty = None
        self.cummulativeQuoteQty = None
        self.status = None
        self.timeInForce = None
        self.type = None
        self.side = None
        self.stopPrice = None
        self.icebergQty = None
        self.time = None
        self.updateTime = None
        self.isWorking = None
        self.workingTime = None
        self.origQuoteOrderQty = None
        self.selfTradePreventionMode = None
        self.__dict__.update(data)

    def __str__(self):
        return ', '.join('%s=%s' % item for item in vars(self).items())
