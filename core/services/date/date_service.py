from datetime import datetime


class DateService:
    @staticmethod
    def timestamp_to_datetime(timestamp: int):
        return datetime.fromtimestamp(timestamp / 1e3)
