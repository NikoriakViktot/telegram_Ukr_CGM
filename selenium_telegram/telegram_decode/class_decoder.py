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

    # def expr(self):
    #     parsed_telegram = {}
    #     error_log = []
    #     token_types = self.get_token_types()
    #     for toktype in token_types:
    #         if toktype in ['GROUP5', 'GROUP6']:
    #             group_values = self.handle_token_types(toktype, error_log)
    #             if group_values is not None:
    #                 parsed_telegram[toktype] = group_values
    #         elif toktype == 'GROUP988':
    #             group_value = self.parse_GROUP988(toktype, error_log)
    #             if group_value is not None:
    #                 parsed_telegram[toktype] = group_value
    #         elif toktype == 'GROUP966':
    #             group_value = self.parse_GROUP966(toktype, error_log)
    #             if group_value is not None:
    #                 parsed_telegram[toktype] = group_value
    #         elif self._accept(toktype):
    #             group_value = self.tok.value
    #             decoding_result = self.decode_and_log_errors(toktype, group_value, error_log)
    #             if decoding_result:
    #                 parsed_telegram[toktype] = decoding_result
    #             if error_log:
    #                     parsed_telegram['errors'] = error_log
    #         # обробка інших типів токенів...
    #     return parsed_telegram
    # def parse_GROUP988(self, toktype, error_log):
    #     if self._accept(toktype):
    #         group_value = self.tok.value
    #         if len(group_value) not in [11]:
    #             error_log.append(
    #                 f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
    #             return
    #         return self.decode_token(toktype, group_value)
    #
    # def parse_GROUP966(self, toktype,error_log):
    #     if self._accept(toktype):
    #         group_value = self.tok.value
    #         if len(group_value) not in [41]:
    #             error_log.append(
    #               f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
    #         tokenizer = HydroTelegramTokenizer(group_value)
    #         parser = Group966Parser(tokenizer)
    #         group_values = parser.parse()
    #         return group_values
    #
    # def parse_GROUP922(self, toktype, error_log):
    #     if self._accept(toktype):
    #         group_value = self.tok.value
    #         tokenizer = HydroTelegramTokenizer(group_value)
    #         parser = Group922Parser(tokenizer)
    #         group_values = parser.parse()
    #         return group_values

# class HydroTelegramParser(Parser):
#     def __init__(self, tokenizer, **kwargs):
#         super().__init__(tokenizer)
#
#     def decoder(self):
#         return DecoderFactory
#
#     def parse(self):
#         parsed_telegram = self.expr()
#         return parsed_telegram
#
#     def decode_token(self, toktype, tokvalue, extra_argument=None):
#         decoder_type = toktype
#         decoder = self.decoder().create_decoder(decoder_type)
#         return decoder.decode(tokvalue)
#
#     def decode_and_log_errors(self, toktype, group_value, error_log):
#         if len(group_value) != 5:
#             error_log.append(f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
#             return
#         decoding_result = self.decode_token(toktype, group_value)
#         return decoding_result
#
#     def handle_token_types(self, toktype, error_log):
#         group_values = []
#         while self._accept(toktype):
#             group_value = self.tok.value
#             decoding_result = self.decode_and_log_errors(toktype, group_value, error_log)
#             if decoding_result:
#                 if decoding_result[1] is None:
#                     group_values.append(decoding_result[0])
#                 if decoding_result[1] is not None:
#                     group_values.append(decoding_result)
#         if group_values:
#             return group_values
#
#     def parse_GROUP988(self, toktype, error_log):
#         if self._accept(toktype):
#             group_value = self.tok.value
#             if len(group_value) not in [11]:
#                 error_log.append(
#                     f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
#                 return
#             return self.decode_token(toktype, group_value)
#
#     def parse_GROUP966(self, toktype,error_log):
#         if self._accept(toktype):
#             group_value = self.tok.value
#             if len(group_value) not in [41]:
#                 error_log.append(
#                   f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
#             tokenizer = HydroTelegramTokenizer(group_value)
#             parser = Group966Parser(tokenizer)
#             group_values = parser.parse()
#             return group_values
#
#     def parse_GROUP922(self, toktype, error_log):
#         if self._accept(toktype):
#             group_value = self.tok.value
#             # if len(group_value) not in [41]:
#             #     error_log.append(
#             #         f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
#             tokenizer = HydroTelegramTokenizer(group_value)
#             parser = Group922Parser(tokenizer)
#             group_values = parser.parse()
#             return group_values
#
#     def expr(self):
#         parsed_telegram = {}
#         error_log = []
#         token_types = ['INDEX', 'DATE_TIME', 'GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7',
#                        'GROUP8', 'GROUP0', 'GROUP988', 'GROUP966', 'GROUP922']
#         for toktype in token_types:
#             if toktype in ['GROUP5', 'GROUP6']:
#                 group_values = self.handle_token_types(toktype, error_log)
#                 if group_values is not None:
#                     parsed_telegram[toktype] = group_values
#             elif toktype == 'GROUP988':
#                 group_value = self.parse_GROUP988(toktype, error_log)
#                 if group_value is not None:
#                     parsed_telegram[toktype] = group_value
#             elif toktype == 'GROUP966':
#                 group_value = self.parse_GROUP966(toktype, error_log)
#                 if group_value is not None:
#                     parsed_telegram[toktype] = group_value
#             elif toktype == 'GROUP922':
#                 group_value = self.parse_GROUP922(toktype, error_log)
#                 if group_value is not None:
#                     parsed_telegram[toktype] = group_value
#             elif self._accept(toktype):
#                 group_value = self.tok.value
#                 decoding_result = self.decode_and_log_errors(toktype, group_value, error_log)
#                 if decoding_result:
#                     parsed_telegram[toktype] = decoding_result
#         if error_log:
#             parsed_telegram['errors'] = error_log
#         return parsed_telegram
