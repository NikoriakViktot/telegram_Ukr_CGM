import datetime


class DateSelect:
    today = datetime.datetime.today()
    timedelta = datetime.timedelta()
    format_spec = "%Y-%m-%d"

    def __init__(self, date):
        self.date_select = date

    def __format__(self, format_spec=''):
        date = self.date_select.strftime(self.format_spec)
        return date

    def __str__(self):
        return str(self.__format__())

    @property
    def date_select(self):
        return self.today + self.timedelta

    @date_select.setter
    def date_select(self, value):
        self.timedelta = datetime.timedelta(days=value)
