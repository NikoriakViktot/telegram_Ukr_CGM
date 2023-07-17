import datetime




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
 