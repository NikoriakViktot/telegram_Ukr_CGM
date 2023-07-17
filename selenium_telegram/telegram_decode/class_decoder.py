from abc import ABC, abstractmethod



# class DecoderContext:
#     def __init__(self, strategy: AbstractDecoder):
#         self._strategy = strategy

#     @property
#     def strategy(self) -> AbstractDecoder:
#         return self._strategy

#     @strategy.setter
#     def strategy(self, strategy: AbstractDecoder) -> None:
#         self._strategy = strategy

#     def execute_strategy(self, value, date_time=None):
#         return self._strategy.decode(value, date_time)
    

#     def decode_telegram(telegram):
#         decoders = {
#             'GROUP1': WaterLevelDecoder(),
#             'GROUP2': LevelChangeDecoder(),
#             # додайте інші декодери тут...
#         }
#         decoder_context = DecoderContext(None)
#         decoded_telegram = {}
#         for group in telegram:
#             if group['type'] in decoders:
#                 decoder_context.strategy = decoders[group['type']]
#                 decoded_telegram[group['type']] = decoder_context.execute_strategy(group['value'], date_time)
#         return decoded_telegram        
    
v = '46450'
s = TemperatureDecoder()
print(s.decode(v))

