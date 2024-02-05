from datetime import datetime


class NvdDatetime(object):

    date_time: datetime

    @classmethod
    def now(cls):
        return cls(datetime.now())

    def __init__(self, date_time: datetime):
        self.date_time = date_time

    def __str__(self):
        return self.date_time.replace(microsecond=0).isoformat() + '.000'

    def __repr__(self):
        return self.date_time.replace(microsecond=0).isoformat() + '.000'
