import datetime
import re

import collections



class SeleniumLogic:
    format_spec_time = "%H:%M:%S"
    format_spec_day = "%Y-%m-%d"
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    date_now = datetime.datetime.today().date()
    time_now = datetime.datetime.today().time()
    

    def __init__(self, **kwargs):
        # super().__init__()
        self.kwargs = kwargs

    @property
    def typeTelegram(self):
        value = self.kwargs.get('typeTelegram')
        return value
    @property
    def indexStation(self):
        value = self.kwargs.get('indexStation')
        return value

    @property
    def numberMessages(self):
        value = self.kwargs.get('numberMessages')
        if value is None:
            return str(self.quantity_messages)
        else:
            return value

   
    @property
    def dateStartingInput(self):
        value = self.kwargs.get('dateStartingInput')
        if value is None:
            return  self.date_now
        else:
            return datetime.date.fromisoformat(value)

    @property
    def dateFinishInput(self):
        value = self.kwargs.get('dateFinishInput')
        if value is None:
            return (self.date_now - datetime.timedelta(2))
        else:
            return datetime.date.fromisoformat(value)
    
    @property
    def quantity_messages(self) -> int:
        delta_date = self.dateStartingInput - self.dateFinishInput
        return delta_date.days   
     

    @property
    def timeStartingInput(self):
        value =  self.kwargs.get('timeStartingInput')
        if value is None:
            return self.time_now
        else:
            return datetime.time.fromisoformat(value)


    @property
    def timeFinishInput(self):
        value = self.kwargs.get('timeFinishInput')
        if value is None:
            return self.time_now
        else:
            return datetime.time.fromisoformat(value)


        
    def date_time_start_input(self):
        start = self.dateStartingInput.strftime(self.format_spec_day) + ' ' + self.timeStartingInput.strftime(self.format_spec_time)
        return (datetime.datetime.strptime(start, self.dt_fmt) + datetime.timedelta(hours=2)).strftime(self.dt_fmt)


    def date_time_finish_input(self):
        finish = self.dateFinishInput.strftime(self.format_spec_day)  + ' ' + self.timeFinishInput.strftime(self.format_spec_time)
        return (datetime.datetime.strptime(finish, self.dt_fmt) + datetime.timedelta(hours=-2)).strftime(self.dt_fmt)


if __name__ == '__main__':
    kwargs= {
        "typeTelegram": 'hydro',
        "indexStation": None,
        "numberMessages": None,
        "dateStartingInput": '2023-05-05',
        "dateFinishInput": '2023-05-01',
        "timeStartingInput": '08:00:00',
        "timeFinishInput": '10:00:00'  }
    d = {'type_telegram': 'hydro', 'index_station': None, 'number_messages': None, 'date_starting_input': None, 'date_finish_input': None, 'time_starting_input': None, 'time_finish_input': None}
    s= SeleniumLogic(**kwargs)
    timeStartingInput = kwargs.get('timeStartingInput')
    timeFinishInput = kwargs.get('timeFinishInput')
    dateFinishInput = kwargs.get('dateFinishInput')
    dateStartingInput = kwargs.get('dateStartingInput')
    numberMessages = kwargs.get('numberMessages')
    indexStation = kwargs.get('indexStation')
    typeTelegram = kwargs.get('typeTelegram')
    print(s.typeTelegram)
    # s.typeTelegram = typeTelegram
    # s.dateStartingInput = dateStartingInput
    # s.timeStartingInput = timeStartingInput
    
    print(s.dateStartingInput)
    print(s.timeStartingInput)
    print(s.dateFinishInput)
    print(s.timeFinishInput)
    print(s.numberMessages)


    print(s.date_time_start_input())
    print(s.date_time_finish_input())
tel = '81801 01081 10350 20021 30360 428// 82234 00000='
p= r'(?P<GROUP4>4\d+|4\d{2}//|4////)'

class Tokenizer:
    Token = collections.namedtuple('Token', ['type', 'value'])
    pattern = r'(?P<WS>\s+)'

    def __init__(self, text, index_station=None, date_time=None):
        self.text = text
        self._setup_paterns(index_station,date_time)


    def _setup_paterns(self, index_station=None, date_time=None):
        self.patterns = [
            r'(?P<WS>\s+)',
            r'(?P<INDEX>{})'.format(index_station),
            r'(?P<DATE_TIME>{}\d{{1}})'.format(date_time),
            r'(?P<GROUP1>1\d+)',
            r'(?P<GROUP2>2\d+)',
            r'(?P<GROUP3>3\d+)',
            r'(?P<GROUP4>4\d+|4\d{2}//|4////)',
            r'(?P<GROUP5>5\d+)',
            r'(?P<GROUP6>6\d+)',
            r'(?P<GROUP7>7\d+)',
            r'(?P<GROUP8>8\d+)',
            r'(?P<GROUP0>0\d{4}|0\d{3}/)',
            r'(?P<GROUP988>988\d{2}\s0\d{4}|988\d{2}\s0\d{3}/)',
            r'(?P<END>=)'
        ]
        self.pattern = '|'.join(self.patterns)

    def generate_tokens(self):
        master_pat = re.compile(self.pattern)
        scanner = master_pat.scanner(self.text)
        print(scanner.match())
        for match_scaner in iter(scanner.match, None):
            if match_scaner.lastgroup == 'WS':
                continue
            yield self.Token(match_scaner.lastgroup, match_scaner.group())



f = Tokenizer(tel)
v = f.generate_tokens()

print(x for x in (x for x in v))