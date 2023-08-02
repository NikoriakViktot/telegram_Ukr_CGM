import re
from abc import ABC, abstractmethod
import collections
from pymetdecoder import synop as s


class TelegramFactory:
    
    @staticmethod
    def create_telegram(type_telegram, **telegram):
        if type_telegram == 'hydro':
            return HydroTelegram(**telegram)
        elif type_telegram == 'meteo':
            return MeteoTelegram(type_telegram,**telegram)
        elif type_telegram == 'shtorm_hydro':
            return ShtormHydroTelegram(**telegram)
        else:
            raise ValueError("Invalid telegram type")

class Tokenizer:
    def __init__(self, text):
        self.text = text
        self.Token = collections.namedtuple('Token', ['type', 'value'])


    def generate_tokens(self, pattern):
        master_pat = re.compile(pattern)
        scanner = master_pat.scanner(self.text)
        for m in iter(scanner.match, None):
            tok = self.Token(m.lastgroup, m.group())
            if tok.type != 'WS':
                yield tok

class HydroTelegramTokenizer(Tokenizer):

    def __init__(self, text, index_station=None, date_time=None):
        super().__init__(text)
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
            r'(?P<GROUP966>966\d{2}\s1\d+\s2\d+\s3\d+\s4\d+\s5\d+\s9\d+)',
            r'(?P<GROUP922>922\d{2}.*)',
            r'(?P<END>=)'
        ]
        self.pattern = '|'.join(self.patterns)

    def generate_tokens(self):
        return super().generate_tokens(self.pattern)

class HydroTelegramTokenizer966(Tokenizer):
    patterns = [
        r'(?P<WS>\s+)',
        r'(?P<GROUP966>966\d{2})',
        r'(?P<GROUP966_1>1\d+)',
        r'(?P<GROUP966_2>2\d+)',
        r'(?P<GROUP966_3>3\d+)',
        r'(?P<GROUP966_4>4\d+)',
        r'(?P<GROUP966_5>5\d+)',
        r'(?P<GROUP966_9>9\d+)']

    def __init__(self, text):
        super().__init__(text)
        self.pattern = '|'.join(self.patterns)

    def generate_tokens(self):
        return super().generate_tokens(self.pattern)


class HydroTelegramTokenizer922(Tokenizer):
    patterns = [
        r'(?P<WS>\s+)',
        r'(?P<GROUP922>922\d{2})',
        r'(?P<GROUP922_1>1\d+)',
        r'(?P<GROUP922_2>2\d+)',
        r'(?P<GROUP922_3>3\d+)',
        r'(?P<GROUP922_4>4\d+|4\d{2}//|4////)',
        r'(?P<GROUP922_5>5\d+)',
        r'(?P<GROUP922_6>6\d+)',
        r'(?P<GROUP922_7>7\d+)',
        r'(?P<GROUP922_8>8\d+)',
        r'(?P<GROUP922_0>0\d{4}|0\d{3}/)',
        r'(?P<END>=)'
    ]

    def __init__(self, text):
        super().__init__(text)
        self.pattern = '|'.join(self.patterns)

    def generate_tokens(self):
        return super().generate_tokens(self.pattern)

class Parser(ABC):
    def __init__(self, tokenizer):
        self.tokens = tokenizer.generate_tokens()
        self.tok = None
        self.nexttok = None
        self._advance()

    def _advance(self):
        self.tok, self.nexttok = self.nexttok, next(self.tokens, None)

    def _accept(self, toktype):
        if self.nexttok and self.nexttok.type == toktype:
            self._advance()
            return True
        else:
            return False

    def _expect(self, toktype):
        if not self._accept(toktype):
            raise SyntaxError('Expected ' + toktype)

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def decoder(self):
        pass

class TelegramParser(Parser):
    def __init__(self, tokenizer, **kwargs):
        super().__init__(tokenizer)

    def decoder(self):
        return DecoderFactory

    def parse(self):
        parsed_telegram = self.expr()
        return parsed_telegram

    def decode_token(self, toktype, tokvalue, extra_argument=None):
        decoder_type = toktype
        decoder = self.decoder().create_decoder(decoder_type)
        return decoder.decode(tokvalue)

    def handle_token_types(self, toktype, error_log):
        group_values = []
        while self._accept(toktype):
            group_value = self.tok.value
            decoding_result = self.decode_and_log_errors(toktype, group_value, error_log)
            if decoding_result and len(decoding_result) > 1 and decoding_result[1] is None:
                group_values.append(decoding_result[0])
            if decoding_result and len(decoding_result) > 1 and decoding_result[1] is not None:
                group_values.append(decoding_result)
        if group_values:
            return group_values

    @abstractmethod
    def get_token_types(self):
        pass

    @abstractmethod
    def get_special_tokens(self):
        pass

class HydroTelegramParser(TelegramParser):
    token_length = {
        'INDEX': 5,
        'DATE_TIME': 5,
        'GROUP1': 5,
        'GROUP2': 5,
        'GROUP3': 5,
        'GROUP4': 5,
        'GROUP5': 5,
        'GROUP6': 5,
        'GROUP7': 5,
        'GROUP8': 5,
        'GROUP0': 5,
        'GROUP988': 11,
        'GROUP966': 41
        # 'GROUP922': 41  # or whatever the correct length is
    }

    def __init__(self, tokenizer, **kwargs):
        super().__init__(tokenizer, **kwargs)


    def decode_and_log_errors(self, toktype, group_value, error_log):
        if len(group_value) != self.token_length[toktype]:
            error_log.append(f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
            return
        decoding_result = self.decode_token(toktype, group_value)
        return decoding_result

    def get_token_types(self):
        return ['INDEX', 'DATE_TIME', 'GROUP1', 'GROUP2', 'GROUP3', 'GROUP4', 'GROUP5', 'GROUP6', 'GROUP7',
                'GROUP8', 'GROUP0', 'GROUP988', 'GROUP966', 'GROUP922']

    def get_special_tokens(self):
        return ['GROUP5', 'GROUP6', 'GROUP988', 'GROUP966', 'GROUP922']

    def parse_token(self, toktype, expected_length, error_log):
        if self._accept(toktype):
            group_value = self.tok.value
            if len(group_value) != expected_length:
                error_log.append(
                    f"Error in {toktype}: incorrect token length {len(group_value)} for value {group_value}")
                return None, None
            return group_value, self.decode_token(toktype, group_value)

    def parse_GROUP988(self, toktype, error_log):
        _, decoded_value = self.parse_token(toktype, 11, error_log)
        return decoded_value

    def parse_group(self, toktype, expected_length, tokenizer_class, parser_class, error_log):
        group_value, decoded_value = self.parse_token(toktype, expected_length, error_log)
        if decoded_value is not None and tokenizer_class is not None and parser_class is not None:
            tokenizer = tokenizer_class(group_value)
            parser = parser_class(tokenizer)
            group_values = parser.parse()
        return group_values

    def parse_GROUP966(self, toktype, error_log):
        return self.parse_group(toktype, 41, HydroTelegramTokenizer966, Group966Parser, error_log)

    # def parse_GROUP922(self, toktype, error_log):
    #     return self.parse_group(toktype, 41, Group922Parser, error_log)
    def expr(self):
        parsed_telegram = {}
        error_log = []
        token_types = self.get_token_types()
        for toktype in token_types:
            if toktype in ['GROUP5', 'GROUP6']:
                group_values = self.handle_token_types(toktype, error_log)
                if group_values is not None:
                    parsed_telegram[toktype] = group_values
            elif toktype == 'GROUP988':
                group_value = self.parse_GROUP988(toktype, error_log)
                if group_value is not None:
                    parsed_telegram[toktype] = group_value
            elif toktype == 'GROUP966':
                group_value = self.parse_GROUP966(toktype, error_log)
                if group_value is not None:
                    parsed_telegram[toktype] = group_value
            elif self._accept(toktype):
                group_value = self.tok.value
                decoding_result = self.decode_and_log_errors(toktype, group_value, error_log)
                if decoding_result:
                    parsed_telegram[toktype] = decoding_result
                if error_log:
                    parsed_telegram['errors'] = error_log

        return parsed_telegram


class Group966Parser(TelegramParser):
    def __init__(self, tokenizer, **kwargs):
        self.tokens = tokenizer.generate_tokens()
        super().__init__(tokenizer, **kwargs)
        self.group966_result = None

    def get_token_types(self):
        return ['GROUP966','GROUP966_1', 'GROUP966_2', 'GROUP966_3',
                'GROUP966_4', 'GROUP966_5', 'GROUP966_9']

    def get_special_tokens(self):
        return []

    def expr(self):
        parsed_telegram = {}
        error_log = []
        token_types = ['GROUP966','GROUP966_1', 'GROUP966_2', 'GROUP966_3',
                       'GROUP966_4', 'GROUP966_5', 'GROUP966_9']
        for toktype in token_types:

            if self._accept(toktype):
                group_value = self.tok.value
                decoded_value = self.decode_token(toktype, group_value)
                if toktype == 'GROUP966':
                    self.group966_result = decoded_value
                elif toktype == 'GROUP966_5':
                    decoded_value['month']=self.group966_result
                    parsed_telegram['obs_time_mesured_dicharge'] = decoded_value
                else:
                    parsed_telegram.update(decoded_value)
        return parsed_telegram

class Group922Parser(TelegramParser):
    def __init__(self, tokenizer, **kwargs):
        self.tokens = tokenizer.generate_tokens_922()
        super().__init__(tokenizer, **kwargs)

    def get_token_types(self):
        return ['GROUP922', 'GROUP922_1', 'GROUP922_2',
                'GROUP922_3', 'GROUP922_4', 'GROUP922_5',
                'GROUP922_6', 'GROUP922_7', 'GROUP922_8', 'GROUP922_0']

    def get_special_tokens(self):
        return ['GROUP922_5', 'GROUP922_6']

    def expr(self):
        parsed_telegram = super().expr()
        return parsed_telegram

# class Group922Parser(Parser):
#
#     def __init__(self, tokenizer, **kwargs):
#
#         self.tokens = tokenizer.generate_tokens_922()  # Assuming you have a generate_tokens_922 method
#         self.tok = None
#         self.nexttok = None
#         self.group922_result = None
#         self._advance()
#
#     def decoder(self):
#         return DecoderFactory
#
#     def parse(self):
#         parsed_telegram = self.expr()
#         print(parsed_telegram)
#         return parsed_telegram
#
#     def decode_token(self, toktype, tokvalue, extra_argument=None):
#         decoder_type = toktype
#         decoder = self.decoder().create_decoder(decoder_type)
#         return decoder.decode(tokvalue)
#
#     def expr(self):
#         parsed_telegram = {}
#         error_log = []
#         token_types = ['GROUP922', 'GROUP922_1', 'GROUP922_2',
#                        'GROUP922_3', 'GROUP922_4', 'GROUP922_5',
#                        'GROUP922_6', 'GROUP922_7', 'GROUP922_8', 'GROUP922_0']
#         for toktype in token_types:
#             if self._accept(toktype):
#                 group_value = self.tok.value
#                 decoded_value = self.decode_token(toktype, group_value)
#                 if toktype == 'GROUP922':
#                     self.group922_result = decoded_value
#                 if toktype in ['GROUP5', 'GROUP6']:
#                     group_values = super().handle_token_types(toktype, error_log)
#                     if group_values is not None:
#                         parsed_telegram[toktype] = group_values
#
#                 # Add more conditions if needed
#         return parsed_telegram


class Telegram(ABC):

    def __init__(self, **kwargs):
        self.index_station = kwargs['index_station']
        self.date_telegram = kwargs['date_telegram']
        self.time_telegram = kwargs['time_telegram']
        self.gauges_telegram = kwargs['gauges_telegram']
        self.date_time = self.date_telegram[8:]+self.time_telegram[:2]
        self.tokenizer = None
        self.parser = None

    @abstractmethod
    def decode_telegram(self):
        pass


class HydroTelegram(Telegram):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tokenizer = HydroTelegramTokenizer(self.gauges_telegram, self.index_station, self.date_time)


    def decode_telegram(self):
        self.parser = HydroTelegramParser(self.tokenizer)
        parsed_data = self.parser.parse()
        return parsed_data

class MeteoTelegram(Telegram):
    CODE_FM_12_IX_SYNOP = 'AAXX'
    Wind_speed_indicator = '1'

    def __init__(self, decoder_type, **kwargs):
        super().__init__(**kwargs)
        self.decoder_type = DecoderFactory.create_decoder(decoder_type)

    def decode_telegram(self):
        station_type = self.CODE_FM_12_IX_SYNOP
        obs_time = self.date_time + self.Wind_speed_indicator
        telegram = station_type + ' ' + obs_time + ' ' + self.gauges_telegram.rstrip('=')
        decoded_telegram = self.decoder_type.decode(telegram)
        return decoded_telegram


class ShtormHydroTelegram(Telegram):
    def interpret(self):
        pass
     
class AbstractDecoder(ABC):

    @abstractmethod
    def decode(self, value):
        pass


    
    def create_dict(self, *args, **kwargs):
       class_name = self.__class__.__name__.replace('Decoder', '')
       key = re.sub(r'(?<!^)(?=[A-Z])', '_', class_name).lower()
       result_dict = {key: dict(zip(args[::2], args[1::2]))}
       for k, v in kwargs.items():
            result_dict[key][k] = v
       return result_dict
       
    
class IndexStationDecoder(AbstractDecoder):
    def decode(self, value):
        return self.create_dict('value', value, 'number_basyen', value[0:2], 'number_station', value[2:])

class ObsTimeDecoder(AbstractDecoder):
    def decode(self, value):
        return self.create_dict('value', value,'day', value[:2], 'hour', value[2:4], 'telegram_section_indicator', value[4])

class WaterLevelDecoder(AbstractDecoder):
    
    def _decode_value(self, value):
        try:
           match int(value[1]):
               case 0 | 1 | 2 | 3 | 4: return int(value[1:5])
               case 5: return -(int(value[2:5]))
               case 6: return -((int(value[2:5])) + 1000)
               case _: return None
        except:
            if len(value) != 5:
                raise ValueError('невірна кількість цифр')

    
    def decode(self, value):
        decod_value = self._decode_value(value)
        try:
           match value[0]:
               case '1': return self.create_dict('value', decod_value, 'unit', 'cm') 
               case '3': return self.create_dict('value', decod_value,
                                    'water_level_time_measured', '20:00',
                                     'unit', 'cm')
               case _ : return decod_value 
        except:
            return None       
                       
class WaterLevelChangeDecoder(AbstractDecoder):
    def _decode_value(self, value):
        try:
            match int(value[4]):
                case 0: return 0
                case 1: return int(value[1:4])
                case 2: return -(int(value[1:4]))
                case _: return None
        except:
            if len(value) != 5:
                raise ValueError('невірна кількість цифр')
            

    def decode(self, value):
        return self.create_dict('value', self._decode_value(value),'unit', 'cm')
    
class TemperatureDecoder(AbstractDecoder):
    def decode(self, value):
        return self.create_dict('value', value[1:], 'water_temperature', self._decode_value_water(value),
                                'air_temperature', self._decode_value_air(value),'unit', 'Cel')
    
    def _decode_value_air(self, value):
        try:
            match value[3]:
                case '5': return -(float(int(value[4]))) 
                case '6': return -(float(int(value[4])+10))
                case '7': return -(float(int(value[4])+20))
                case '8': return -(float(int(value[4])+30))
                case '9': return -(float(int(value[4])+40))
                case _: return float(int(value[3:]))
        except:
            return  None
        
    
    def  _decode_value_water(self,value):
        try:
           return float(int(value[1:3]))
        except:
            return None

class BaseConditionDecoder(AbstractDecoder):
    
    data_dict = {}
    intensity_dict= {
    "01": "10%",
    "02": "20%",
    "03": "30%",
    "04": "40%",
    "05": "50%",
    "06": "60%",
    "07": "70%",
    "08": "80%",
    "09": "90%",
    "10": "100%"
    }
    
    def decode(self, token_type, value):
  
        key1 = value[1:3]
        key2 = value[3:5]
        intensity_key = value[3:5]
        intensity = self.intensity_dict.get(intensity_key)

        def create_dict(key, intensity):
            data = self.data_dict.get(key)
            if data is not None:
                result_dict = {
                    'value': key,
                    'description_en': data['description_en'],
                    'description_uk': data['description_uk'],
                }
                if data['intensity']:
                    if intensity is not None:
                        result_dict['intensity'] = intensity
                    else:
                        result_dict['error'] = f"Error: Phenomenon {key} requires intensity but none provided in value {value}"
                return result_dict
            else:
                data = self.data_dict.get(key)
                if data is not None and data['intensity'] == False:
                    return {'error': f"Error: Invalid value key {key}"}
        
        result1 = create_dict(key1, intensity)
        result2 = create_dict(key2, None) if key1 != key2 else None
        return [result1, result2]
     
class IcePhenomenaDecoder(BaseConditionDecoder):

    data_dict = {
    '11': {'intensity': False, 'description_en': 'Fat', 'description_uk': 'Сало'},
    '12': {'intensity': True, 'description_en': 'Snowslide', 'description_uk': 'Сніжура'},
    '13': {'intensity': True, 'description_en': 'Shore ice', 'description_uk': 'Забереги'},
    '14': {'intensity': False, 'description_en': 'Ice floe with a width over 100m', 'description_uk': 'Припай шириною більше 100м'},
    '15': {'intensity': False, 'description_en': 'Overhanging ice on the shore', 'description_uk': 'Забереги навислі'},
    '16': {'intensity': True, 'description_en': 'Icebreaker', 'description_uk': 'Льодохід'},
    '17': {'intensity': True, 'description_en': 'Icebreaker', 'description_uk': 'Льодохід'},
    '18': {'intensity': False, 'description_en': 'Icebreaker over the ice cover', 'description_uk': 'Льодохід поверх льдового покриву'},
    '19': {'intensity': True, 'description_en': 'Ice ridge', 'description_uk': 'Шугохід'},
    '20': {'intensity': False, 'description_en': 'Intra-ice', 'description_uk': 'Внутрішньоводний лід'},
    '21': {'intensity': False, 'description_en': 'Pyatry', 'description_uk': "П'ятри"},
    '22': {'intensity': False, 'description_en': 'Raised ice', 'description_uk': 'Осівший лід'},
    '23': {'intensity': False, 'description_en': 'Ice avalanches on the shore', 'description_uk': 'Навали льоду на березі'},
    '24': {'intensity': False, 'description_en': 'Ice dam in the post area', 'description_uk': 'Льодова перемичка у створі поста'},
    '25': {'intensity': False, 'description_en': 'Ice dam above the post', 'description_uk': 'Льодова перемичка вище поста'},
    '26': {'intensity': False, 'description_en': 'Ice dam below the post', 'description_uk': 'Льодова перемичка нижче поста'},
    '30': {'intensity': False, 'description_en': 'Ice jam above the post', 'description_uk': 'Затор льоду вище поста'},
    '31': {'intensity': False, 'description_en': 'Ice jam below the post', 'description_uk': 'Затор льоду нижче поста'},
    '32': {'intensity': False, 'description_en': 'Ice jam artificially destroyed', 'description_uk': 'Затор льоду штучно руйнується'},
    '34': {'intensity': False, 'description_en': 'Ice jam above the station', 'description_uk': 'Зажор льоду вище поста'},
    '35': {'intensity': False, 'description_en': 'Ice jam below the station', 'description_uk': 'Зажор льоду нижче поста'},
    '36': {'intensity': False, 'description_en': 'Ice jam artificially destroyed', 'description_uk': 'Зажор льоду штучно руйнується'},
    '37': {'intensity': False, 'description_en': 'Water on the ice', 'description_uk': 'Вода на льоду'},
    '38': {'intensity': False, 'description_en': 'Water flowing on the ice', 'description_uk': 'Вода тече поверх льоду'},
    '39': {'intensity': True, 'description_en': 'Edges', 'description_uk': 'Закраїни'},
    '40': {'intensity': False, 'description_en': 'Ice darkened', 'description_uk': 'Лід потемнів'},
    '41': {'intensity': False, 'description_en': 'Snow dust', 'description_uk': 'Сніжниця'},
    '42': {'intensity': False, 'description_en': 'Ice lifted', 'description_uk': 'Лід підняло'},
    '43': {'intensity': False, 'description_en': 'Ice movement', 'description_uk': 'Посування льоду'},
    '44': {'intensity': False, 'description_en': 'Ice ridge', 'description_uk': 'Розводдя'},
    '45': {'intensity': False, 'description_en': 'Ice melting in place', 'description_uk': 'Лід тане на місці'},
    '46': {'intensity': True, 'description_en': 'Residual ice on the shore', 'description_uk': 'Забереги залишкові'},
    '47': {'intensity': False, 'description_en': 'Ice drift', 'description_uk': 'Наслуд'},
    '48': {'intensity': True, 'description_en': 'Broken ice', 'description_uk': 'Битий лід'},
    '49': {'intensity': True, 'description_en': 'Crushed ice', 'description_uk': 'Млинчастий лід'},
    '50': {'intensity': True, 'description_en': 'Ice fields', 'description_uk': 'Льодяні поля'},
    '51': {'intensity': False, 'description_en': 'Slush', 'description_uk': 'Льодяна каша'},
    '52': {'intensity': False, 'description_en': 'Frazil ice', 'description_uk': 'Стамуха'},
    '53': {'intensity': False, 'description_en': 'Ice moving away from the shore', 'description_uk': 'Лід відносить від берега'},
    '54': {'intensity': False, 'description_en': 'Ice pressed against the shore', 'description_uk': 'Лід притиснуло до берега'},
    '63': {'intensity': True, 'description_en': 'Incomplete ice cover', 'description_uk': 'Льодостав неповний'},
    '64': {'intensity': True, 'description_en': 'Ice cover with polynyas', 'description_uk': 'Льодовий покрив з ополонками'},
    '65': {'intensity': False, 'description_en': 'Ice cover', 'description_uk': 'Льодостав'},
    '66': {'intensity': False, 'description_en': 'Ice cover with floes', 'description_uk': 'Льодостав з торосами'},
    '67': {'intensity': False, 'description_en': 'Ice cover with ridges of floes', 'description_uk': 'Льодовий покрив з грядами торосів'},
    '68': {'intensity': False, 'description_en': 'Slush track', 'description_uk': 'Шугова доріжка'},
    '69': {'intensity': False, 'description_en': 'Silt under the ice', 'description_uk': 'Під льодом шуга'},
    '70': {'intensity': False, 'description_en': 'Cracks in the ice cover', 'description_uk': 'Тріщини у льодовому покриві'},
    '71': {'intensity': False, 'description_en': 'Open water', 'description_uk': 'Полій'},
    '72': {'intensity': False, 'description_en': 'Overhanging ice', 'description_uk': 'Лід навислий'},
    '73': {'intensity': False, 'description_en': 'Layered ice', 'description_uk': 'Лід ярусний'},
    '74': {'intensity': False, 'description_en': 'Ice on the bottom', 'description_uk': 'Лід на дні'},
    '75': {'intensity': False, 'description_en': 'River frozen', 'description_uk': 'Річка промерзла'},
    '76': {'intensity': False, 'description_en': 'Ice artificially destroyed', 'description_uk': 'Лід штучно зруйновано'},
    '77': {'intensity': False, 'description_en': 'Ponded water', 'description_uk': 'Полійна вода'}
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_type = 'ice_phenomena'
    
    def decode(self, value):
       return super().decode(self.token_type, value)
    
class WaterBodyConditionDecoder(BaseConditionDecoder):
    data_dict  = {
    "00": {'intensity': False, 'description_en': 'Clean', 'description_uk': 'Чисто'},
    "11": {'intensity': True, 'description_en': 'Timber rafting', 'description_uk': 'Лісосплав'},
    "14": {'intensity': False, 'description_en': 'Forest bend above the station', 'description_uk': 'Залом лісу вище поста'},
    "15": {'intensity': False, 'description_en': 'Forest bend below the station', 'description_uk': 'Залом лісу нижче поста'},
    "22": {'intensity': True, 'description_en': 'Vegetation near the shore', 'description_uk': 'Рослинність біля берега'},
    "23": {'intensity': True, 'description_en': 'Vegetation across the river section', 'description_uk': 'Рослинність по всьому перерізу річки'},
    "24": {'intensity': True, 'description_en': 'Vegetation in patches across the stream section', 'description_uk': 'Рослинність по перерізу потоку плямами'},
    "25": {'intensity': False, 'description_en': 'Vegetation spreading along the bottom', 'description_uk': 'Рослинність стелеться по дну'},
    "26": {'intensity': False, 'description_en': 'Vegetation mowed in the water column', 'description_uk': 'Рослинність у гідростворі викошена'},
    "27": {'intensity': False, 'description_en': 'Vegetation lying on the bottom', 'description_uk': 'Рослинність лягла на дно'},
    "28": {'intensity': False, 'description_en': 'Vegetation covered with silt', 'description_uk': 'Рослинність занесено мулом'},
    "29": {'intensity': False, 'description_en': 'Vegetation died due to river pollution', 'description_uk': 'Рослинність загинула в результаті забруднення річки'},
    "35": {'intensity': False, 'description_en': 'Bank collapse (erosion) in the station pool', 'description_uk': 'Обвал (зсув) берега у сворі поста'},
    "36": {'intensity': False, 'description_en': 'Bank collapse (erosion) above the station', 'description_uk': 'Обвал (зсув) берега вище поста'},
    "37": {'intensity': False, 'description_en': 'Bank collapse (erosion) below the station', 'description_uk': 'Обвал (зсув) берега нижче поста'},
    "38": {'intensity': False, 'description_en': 'Channel dredging works', 'description_uk': 'Днопоглиблювальні роботи в руслі'},
    "39": {'intensity': False, 'description_en': 'Channel embankment works', 'description_uk': 'Намивні роботи в руслі'},
    "40": {'intensity': False, 'description_en': 'Channel cleared', 'description_uk': 'Русло розчищено'},
    "41": {'intensity': False, 'description_en': 'River channel narrowed in the water column for water flow measurement', 'description_uk': 'Русло річки звужено в гідростворі для вимірювання витрат води'},
    "42": {'intensity': False, 'description_en': 'Sandbank formed', 'description_uk': 'Утворилася коса'},
    "43": {'intensity': False, 'description_en': 'Sandbank', 'description_uk': 'Коса'},
    "44": {'intensity': False, 'description_en': 'Eddy formed', 'description_uk': 'Утворився осередок'},
    "45": {'intensity': False, 'description_en': 'Eddy', 'description_uk': 'Осередок'},
    "46": {'intensity': False, 'description_en': 'Island formed', 'description_uk': 'Утворився острів'},
    "47": {'intensity': False, 'description_en': 'Island', 'description_uk': 'Острів'},
    "48": {'intensity': False, 'description_en': 'Shift in the channel in the plan', 'description_uk': 'Зміщення русла у плані'},
    "52": {'intensity': False, 'description_en': 'Channel overgrown with reeds', 'description_uk': 'Русло заросло очеретом'},
    "53": {'intensity': True, 'description_en': 'Reeds in the channel', 'description_uk': 'Очерет у руслі'},
    "54": {'intensity': True, 'description_en': 'Reeds in the channel above the station', 'description_uk': 'Очерет у руслі вище поста'},
    "55": {'intensity': True, 'description_en': 'Reeds in the channel below the station', 'description_uk': 'Очерет у руслі нижче поста'},
    "56": {'intensity': False, 'description_en': 'Debris flow passage', 'description_uk': 'Проходження селевого потоку'},
    "57": {'intensity': False, 'description_en': 'River flow changed to opposite direction', 'description_uk': 'Течія річки змінилася на протилежну'},
    "59": {'intensity': False, 'description_en': 'Water surge', 'description_uk': 'Нагін води'},
    "60": {'intensity': False, 'description_en': 'River dried up', 'description_uk': 'Річка пересохла'},
    "61": {'intensity': False, 'description_en': 'Weak waves (1 point)', 'description_uk': 'Хвилювання слабке (1 бал)'},
    "62": {'intensity': False, 'description_en': 'Moderate waves (2-3 points)', 'description_uk': 'Хвилювання помірне (2-3 бали)'},
    "63": {'intensity': False, 'description_en': 'Strong waves (more than 4 points)', 'description_uk': 'Хвилювання сильне (більше 4 балів)'},
    "64": {'intensity': False, 'description_en': 'Stagnant water', 'description_uk': 'Стояча вода'},
    "65": {'intensity': False, 'description_en': 'Stagnant water under the ice', 'description_uk': 'Стояча вода під льодом'},
    "66": {'intensity': False, 'description_en': 'Boat crossing stopped', 'description_uk': 'Припинилась переправа на човнах'},
    "67": {'intensity': False, 'description_en': 'Pedestrian traffic on ice stopped', 'description_uk': 'Припинилося пішоходне сполучення по льоду'},
    "68": {'intensity': False, 'description_en': 'Pedestrian traffic on ice started', 'description_uk': 'Розпочалося пішоходне сполучення по льоду'},
    "69": {'intensity': False, 'description_en': 'Transportation on ice started', 'description_uk': 'Розпочався рух транспорту на льоду'},
    "70": {'intensity': False, 'description_en': 'Transportation on ice stopped', 'description_uk': 'Припинився рух транспорту на льоду'},
    "71": {'intensity': False, 'description_en': 'Boat crossing started', 'description_uk': 'Розпочалася переправа човнами'},
    "72": {'intensity': False, 'description_en': 'Shore support from the river, reservoir, lake', 'description_uk': 'Підпір від річки, водосховища, озера'},
    "73": {'intensity': False, 'description_en': 'Navigation start', 'description_uk': 'Початок навігації'},
    "74": {'intensity': False, 'description_en': 'Navigation end', 'description_uk': 'Закінчення навігації'},
    "77": {'intensity': False, 'description_en': 'Water intake above the station', 'description_uk': 'Забір води вище поста'},
    "78": {'intensity': False, 'description_en': 'Water intake below the station', 'description_uk': 'Забір води нижче поста'},
    "79": {'intensity': False, 'description_en': 'Water intake above the station stopped', 'description_uk': 'Забір води вище поста припинився'},
    "80": {'intensity': False, 'description_en': 'Water intake below the station stopped', 'description_uk': 'Забір води нижче поста припинився'},
     "81": {'intensity': False, 'description_en': 'Water discharge above the station', 'description_uk': 'Скид води вище поста'},
    "82": {'intensity': False, 'description_en': 'Water discharge below the station', 'description_uk': 'Скид води нижче поста'},
    "83": {'intensity': False, 'description_en': 'Water discharge above the station stopped', 'description_uk': 'Скид води вище поста припинився'},
    "84": {'intensity': False, 'description_en': 'Water discharge below the station stopped', 'description_uk': 'Скид води нижче поста припинився'},
    "85": {'intensity': False, 'description_en': 'Dam (weir) above the station', 'description_uk': 'Гребля (перетинка, загата, дамба) вище поста'},
    "86": {'intensity': False, 'description_en': 'Dam (weir) below the station', 'description_uk': 'Гребля (перетинка, загата, дамба) нижче поста'},
    "87": {'intensity': False, 'description_en': 'Dam (weir) above the station destroyed', 'description_uk': 'Зруйнована гребля (перетинка, загата, дамба) вище поста'},
    "88": {'intensity': False, 'description_en': 'Dam (weir) below the station destroyed', 'description_uk': 'Зруйнована гребля (перетинка, загата, дамба) нижче поста'},
    "89": {'intensity': False, 'description_en': 'Channel support from debris obstruction', 'description_uk': 'Підпір від засмічення (захаращення) русла'},
    "90": {'intensity': False, 'description_en': 'Channel support from bridge crossings', 'description_uk': 'Підпір від мостових переправ'},
    "91": {'intensity': False, 'description_en': 'Water discharge from the reservoir', 'description_uk': 'Пропуски води з водосховища'}
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token_type = 'water_body_condition'

    def decode(self, value):
        return super().decode(self.token_type, value)       

class IceThicknessDecoder(AbstractDecoder):
    data_height = {
    "0": {'height_en': 'No snow on the ice', 'height_uk': 'На льоду снігу немає'},
    "1": {'height_en': '>  5 cm', 'height_uk': '>  5 см'},
    "2": {'height_en': '5 - 10 cm', 'height_uk': '5 - 10 см'},
    "3": {'height_en': '11 - 15 cm', 'height_uk': '11 - 15 см'},
    "4": {'height_en': '16 - 20 cm', 'height_uk': '16 - 20 см'},
    "5": {'height_en': '21 - 25 cm', 'height_uk': '21 - 25 см'},
    "6": {'height_en': '26 - 35 cm', 'height_uk': '26 - 35 см'},
    "7": {'height_en': '36 - 50 cm', 'height_uk': '36 - 50 см'},
    "8": {'height_en': '51 - 70 cm', 'height_uk': '51 - 70 см'},
    "9": {'height_en': '< 70 cm', 'height_uk': '< 70 см'},
      }
    
    def _decode_value_ice(self, value):
        ice_thickness =  value[1:4]
        return {'value_ice': ice_thickness,'ice_thickness':int(ice_thickness)}
    
    def _decode_value_snow(self, value):
        snow_height =  value[4]
        data = self.data_height.get(snow_height)
        dict_val = {'value_snow':snow_height}
        if data is not None:
            return {**dict_val, **data}  
        return {} 

    def decode(self, value):
        unit = {'unit':'cm'}
        return self.create_dict(**self._decode_value_ice(value), 
                                **self._decode_value_snow(value),
                                **unit)

class DecoderIntegerPart:
    def decode_value(self, value):
        try:
            match int(value[1]):
                case 0: return float(int(value[2:5]) / 1000)
                case 1: return float(int(value[2:5]) / 100)
                case 2: return float((int(value[2:5])) / 10)
                case 3: return float(value[2:5])
                case 4: return float(int(value[2:5]) * 10)
                case 5: return float(int(value[2:5]) * 100)
                case _: return None
        except:
            return None

class WaterDischargeDecoder(AbstractDecoder, DecoderIntegerPart):

    def decode(self, value):
        return self.create_dict('value', self.decode_value(value),
                                'unit', 'm³/s')

class PrecipitationMixin:

    def precipitation_decode(self, value):
        try:
            
            match value[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value[2:4]) - 90)/10)
                case _: return float(value[1:4])

        except:
            return None
    
    def precip_intens_decode(self, value):
        try:
            if self.precipitation_decode(value) is not None: 
                match value[4]:
                    case '0': return '> 1'
                    case '1': return '1 - 3'
                    case '2': return '3 - 6'
                    case '3': return '6 - 12'
                    case '4': return '< 12'
                    case '/': return None
                    case _:   return None

        except:
            return None
        
class DailyPrecipitationDecoder(PrecipitationMixin, AbstractDecoder):
    
    def decode(self, value):
        precip_value = self.precipitation_decode(value)
        precip_intens_value = self.precip_intens_decode(value)
        return self.create_dict('value_telegram', value,
                                'precipitation', precip_value,
                                'precipitation_intensity', precip_intens_value,
                                'unit', 'mm')
     
class DailyDaytimePrecipitationDecoder(PrecipitationMixin, AbstractDecoder):
      
    def get_precip_day_group(self, value):
        value_day = value.split()[0]  
        value_precipitation = value.split()[1]  
        return value_day, value_precipitation

    def decode(self, value):
        precip_value = self.precipitation_decode(self.get_precip_day_group(value)[1])
        precip_intens_value = self.precip_intens_decode(self.get_precip_day_group(value)[1])
        precipitation_date = self.get_precip_day_group(value)[0][3:5]
        return self.create_dict('value_telegram', value,
                                'precipitation_date', precipitation_date, 
                                'precipitation_time_measured', '20:00',
                                'precipitation', precip_value,
                                'precipitation_intensity', precip_intens_value,
                                'unit', 'mm')
     
class MeasuredWaterDischargeDecoder(AbstractDecoder):

    def decode(self, value):
        month = value[3:5]
        return month

class ObsTimeMesuredDichargeDecoder(AbstractDecoder):

    def decode(self, value):
        return {'month': None,
            'day':value[1:3],
                'hour': value[3:5]}

class AreaWaterSectionDecoder(AbstractDecoder, DecoderIntegerPart):

    def decode(self, value):
        return self.create_dict('value', self.decode_value(value),
                                'unit', 'm²')

class MaxDeepRiverDecoder(AbstractDecoder):

    def decode(self, value):
        return self.create_dict('value', int(value[1:]), 'unit', 'cm')

class MaxSpeedFlowingDecoder(AbstractDecoder, DecoderIntegerPart):

    def decode(self, value):
        return self.create_dict('value', self.decode_value(value), 'unit', 'm/s' )

class MeteoDecoder(AbstractDecoder):

    def __init__(self):
        self.decoder = s.SYNOP()

    def decode(self, telegram):
        return self.decoder.decode(telegram)
    
class DecoderFactory:
    decoders = {
            'meteo': MeteoDecoder,
            'INDEX': IndexStationDecoder,
            'DATE_TIME': ObsTimeDecoder,
            'GROUP1': WaterLevelDecoder,
            'GROUP2': WaterLevelChangeDecoder,
            'GROUP3': WaterLevelDecoder,
            'GROUP4': TemperatureDecoder,
            'GROUP5': IcePhenomenaDecoder,
            'GROUP6': WaterBodyConditionDecoder,
            'GROUP7': IceThicknessDecoder,
            'GROUP8': WaterDischargeDecoder,
            'GROUP0': DailyPrecipitationDecoder,
            'GROUP988': DailyDaytimePrecipitationDecoder,
            'GROUP966': MeasuredWaterDischargeDecoder,
            'GROUP966_1': WaterLevelDecoder,
            'GROUP966_2': WaterDischargeDecoder,
            'GROUP966_3': AreaWaterSectionDecoder,
            'GROUP966_4': MaxDeepRiverDecoder,
            'GROUP966_5': ObsTimeMesuredDichargeDecoder,
            'GROUP966_9': MaxSpeedFlowingDecoder }
    
    
    @classmethod
    def create_decoder(cls, type_decoder):
        decoder_class = cls.decoders.get(type_decoder)
        if decoder_class:
            return decoder_class()
        else:
            raise ValueError(f"Decoder type '{type_decoder}' not recognized")
        

d ={'date_telegram': '2023-06-04', 
    'time_telegram': '08:00:00', 
    'index_station': '81041',
    'gauges_telegram': '81041 04081 10262 20062 30265 41212 51910 56565 51305 82980 09911 98803 00023 96606 15042 20650 31725 40075 50714 90210='}
m = {'date_telegram': '2023-06-04', 
    'time_telegram': '08:00:00', 
    'index_station': '81041',
    'gauges_telegram':'33658 42984 03101 10261 20122 39805 40082 57003 555 1/044='}
import pprint

telegram_obj = TelegramFactory.create_telegram('hydro', **d)
decoded_telegram = telegram_obj.decode_telegram()
pprint.pprint([x for x in telegram_obj.tokenizer.generate_tokens()])
pprint.pprint(decoded_telegram)
# telegram_obj_m = TelegramFactory.create_telegram('meteo', **m)
# decoded_telegram_n = telegram_obj_m.decode_telegram()
# pprint.pprint(decoded_telegram_n)

