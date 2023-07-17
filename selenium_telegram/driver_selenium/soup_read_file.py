import re
from bs4 import BeautifulSoup
from typing import NamedTuple
from requests_html import HTML

from .html_telegrame import SaveHtmlFile
from .class_date_select import DateSelect


class TelegramReportNamedtuple(NamedTuple):
    id_telegrame: str
    index_station: str
    date_telegram: str
    time_telegram: str
    gauges_telegrame: str = None


class SoupHtmlFile:
    date_now = format(DateSelect(0))
    date_last = format(DateSelect(-1))
    html_obj = None

    @classmethod
    def get_html_obj(cls, html):
        if cls.html_obj is None:
            html_str = html
            cls.html_obj = HTML(html=html_str)
        return cls.html_obj

    # @classmethod
    # def file(cls):
    #     return SaveHtmlFile.get_html_obj()

    @classmethod
    def file_object(cls):
        return SaveHtmlFile.open_html_file()

    @classmethod
    def soup_file(cls):
        soup = BeautifulSoup(cls.file_object(), 'html.parser')
        body_telegrame = soup.find_all('pre')
        return body_telegrame

    # def soup_file(cls, file):
    #     soup = BeautifulSoup(cls.get_html_obj(html=file), 'html.parser')
    #     body_telegrame = soup.find_all('pre')
    #     return body_telegrame

    @classmethod
    def clear_data(cls):
        telegram_ = [re.sub(("\s+"), " ", i) for i in ['='.join(i) for i in cls.soup_file()]]
        return telegram_

    @classmethod
    def slice_telegram(cls):
        value = cls.clear_data()
        index_telegram = slice(20, 25)
        date_telegram = slice(0, 10)
        time_telegram = slice(11, 19)
        telegram = slice(20, None)
        tuple_telegram = [(x[index_telegram] +
                           x[date_telegram].replace('-', '') +
                           x[time_telegram].replace(':', ''),
                           x[index_telegram],
                           x[date_telegram],
                           x[time_telegram],
                           x[telegram]) for x in value]
        return tuple_telegram

    def report(self):
        return (TelegramReportNamedtuple(*x) for x in self.slice_telegram())

    def telegram_today(self):
        for x in self.report():
            var = x.date_telegram == self.date_now
            if var is True:
                telegram_today = {
                             'id_telegrame': x.id_telegrame,
                             'index_station': x.index_station,
                             'date_telegram': x.date_telegram,
                             'time_telegram': x.time_telegram,
                             'gauges_telegrame': x.gauges_telegrame}
                yield telegram_today

    def telegram_yesterday(self):
        for x in self.report():
            var = x.date_telegram == self.date_last
            if var is True:
                telegram_yesterday = {
                               'id_telegrame': x.id_telegrame,
                               'index_station': x.index_station,
                               'date_telegram': x.date_telegram,
                               'time_telegram': x.time_telegram,
                               'gauges_telegrame': x.gauges_telegrame}
                yield telegram_yesterday
