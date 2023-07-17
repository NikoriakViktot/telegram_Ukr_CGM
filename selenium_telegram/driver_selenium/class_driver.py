import time
import datetime
import json
import base64
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from pymongo import MongoClient

from driver_selenium.soup_read_file import SoupHtmlFile
from .UKR_CGM_webelement import *
from .html_telegrame import SaveHtmlFile
from mongo_db.mongo_tools import MongoDb
from telegram_decode.gidro_kod_KC15 import KC15
from telegram_decode.class_telegrame import TelegramFactory

MONGO_URL='mongodb://mongo:27017/'
client = MongoClient(MONGO_URL)
db = MongoDb

def get_user_agent():
    return UserAgent(verify_ssl=False).random

class TelegramParser:
    driver: WebDriver = None
    url = 'http://gcst.meteo.gov.ua/armua/sino/index.phtml'
    user = 'chernovcgm'
    password = "(zBLFX$#)b"
    actions = ActionChains(driver)  
    format_spec_time = "%H:%M:%S"
    format_spec_day = "%Y-%m-%d"
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    date_now = datetime.datetime.today().date()
    time_now = datetime.datetime.today().time()
    __list_station_hydro = ['42130', '42136', '42137', '42148', '42176', '42187', '42194', '42198', '42201', '42202',
                            '42249', '42256', '42802', '42803', '44006', '44007', '44019', '44025', '44028', '44031',
                            '44033', '44034', '44036', '44038', '44046', '44050', '44051', '44054', '44062', '44064',
                            '44067', '44073', '44079', '44080', '44083', '44085', '44087', '44090', '44093', '44096',
                            '44098', '44100', '44108', '44110', '44113', '44116', '44120', '44121', '44124', '44130',
                            '78281', '78285', '78288', '78289', '78291', '78293', '78295', '78301', '78309', '78324',
                            '78326', '78351', '78361', '78365', '78371', '78376', '78397', '78399', '78413', '78421',
                            '78427', '78430', '78434', '78436', '78439', '78443', '78445', '78450', '78471', '79043',
                            '79358', '79360', '79361', '79365', '79397', '79400', '79403', '79405', '79407', '79416',
                            '79424', '79473', '79477', '79485', '79491', '79496', '79513', '79516', '79518', '79521',
                            '79524', '79538', '79543', '79545', '79549', '79555', '79557', '79584', '79596', '79694',
                            '79701', '79723', '79726', '79747', '79753', '79755', '79757', '79761', '79763', '80073',
                            '80077', '80083', '80084', '80088', '80090', '80099', '80123', '80131', '80136', '80179',
                            '80183', '80193', '80209', '80255', '80259', '80272', '80280', '80285', '80289', '80292',
                            '80295', '80302', '80320', '80344', '80346', '80350', '80354', '80355', '80359', '80369',
                            '80372', '80380', '80386', '80391', '80395', '80401', '80408', '80412', '80421', '80432',
                            '80436', '80447', '80453', '80460', '80473', '80478', '80483', '80486', '80494', '80505',
                            '80516', '80524', '80527', '80530', '80561', '80564', '80568', '80598', '80600', '80605',
                            '81011', '81015', '81017', '81028', '81030', '81033', '81041', '81052', '81078', '81080',
                            '81085', '81087', '81092', '81097', '81102', '81103', '81108', '81113', '81120', '81122',
                            '81126', '81129', '81140', '81147', '81151', '81152', '81156', '81161', '81169', '81172',
                            '81178', '81184', '81191', '81197', '81199', '81203', '81205', '81206', '81209', '81210',
                            '81213', '81215', '81219', '81225', '81230', '81232', '81236', '81241', '81242', '81243',
                            '81244', '81245', '81249', '81250', '81251', '81254', '81257', '81267', '81338', '81346',
                            '81348', '81353', '81361', '81363', '81365', '81381', '81386', '81393', '81396', '81408',
                            '81414', '81417', '81421', '81430', '81433', '81438', '81439', '81446', '81449', '81450',
                            '81465', '81468', '81469', '81471', '81472', '81474', '81475', '81562', '81565', '81580',
                            '81581', '81592', '81593', '81597', '81600', '81604', '81616', '81640', '81648', '81674',
                            '81677', '81686', '81691', '81692', '81693', '81694', '81717', '81724', '81730', '81737',
                            '81741', '81745', '81748', '81750', '81753', '81757', '81767', '81772', '81801', '83006',
                            '83012', '83019', '83022', '83026', '83027', '83028', '83035', '83036', '83040', '83045',
                            '83048', '83050', '83068', '83074', '83083']
    __list_station_meteo = ['33958', '33889', '33994', '33182', '33995', '33049', '33058', '33067', '33075',
                            '33088', '33135', '33136', '33146', '33156', '33173', '33177', '33187', '33203',
                            '33213', '33215', '33228', '33231', '33236', '33246', '33261', '33268', '33275',
                            '33287', '33288', '33296', '33297', '33299', '33301', '33312', '33317', '33325',
                            '33339', '33342', '33345', '33347', '33354', '33356', '33362', '33376', '33377',
                            '33382', '33391', '33392', '33393', '33398', '33409', '33415', '33421', '33429',
                            '33439', '33446', '33464', '33466', '33475', '33484', '33487', '33495', '33506',
                            '33511', '33513', '33514', '33515', '33516', '33517', '33518', '33524', '33526',
                            '33536', '33548', '33557', '33562', '33564', '33577', '33581', '33586', '33587',
                            '33593', '33598', '33605', '33609', '33614', '33621', '33631', '33633', '33634',
                            '33638', '33645', '33646', '33647', '33651', '33657', '33658', '33662', '33663',
                            '33686', '33699', '33705', '33711', '33717', '33719', '33723', '33759', '33761',
                            '33777', '33788', '33791', '33801', '33805', '33830', '33833', '33834', '33835',
                            '33836', '33846', '33848', '33862', '33869', '33877', '33887', '33896', '33898',
                            '33902', '33907', '33910', '33915', '33917', '33922', '33924', '33929', '33933',
                            '33934', '33939', '33945', '33946', '33957', '33959', '33961', '33962', '33966',
                            '33973', '33976', '33981', '33983', '33986', '33990', '33991', '33998', '34208',
                            '34300', '34302', '34304', '34312', '34317', '34319', '34320', '34329', '34401',
                            '34407', '34409', '34415', '34421', '34434', '34502', '34504', '34505', '34509',
                            '34510', '34514', '34519', '34523', '34524', '34537', '34601', '34606', '34607',
                            '34609', '34615', '34622', '34704', '34708', '34712', '34717']
    request = {}
    user = 'chernovcgm'
    password = "(zBLFX$#)b"
    url = 'http://gcst.meteo.gov.ua/armua/sino/index.phtml'
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.driver = self.get_driver()
        self.execute_cmd("Network.enable", {})
        # load_dotenv()
        self.execute_cmd("Network.setExtraHTTPHeaders",
                         {"headers": self.get_auth_header(self.user, self.password)})
        self.get_with_retry()

    @classmethod
    def get_driver(cls):
        if cls.driver is None:
            cls.restart_session()
        return cls.driver
       
    
    @classmethod
    def restart_session(cls):
        if cls.driver is not None:
            cls.driver.quit()
        user_agent = get_user_agent()
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
        options.add_argument(f"user-agent={user_agent}")
        service = Service(executable_path='/usr/local/bin/')
        driver = webdriver.Chrome(service=service, options=options)
        cls.driver = driver
        cls.actions = ActionChains(driver) 
        return cls.driver

    @classmethod       
    def get_with_retry(cls, max_retries=3, retry_interval=900):
        retries = 0
        while retries < max_retries:
            try:
                cls.driver.get(cls.url)
                return  
            except Exception as e:
                print(f"Помилка при з'єднанні з сервером: {str(e)}")
                print(f"Повторна спроба з'єднанні з сервером через {retry_interval} ceк.")
                time.sleep(retry_interval)
                retries += 1
        print("Досягнуто максимальну кількість спроб. Виконання запиту не вдалося.")


    @staticmethod
    def get_auth_header(user, password):
        b64 = "Basic " + base64.b64encode('{}:{}'.format(user, password).encode('utf-8')).decode('utf-8')
        return {"Authorization": b64}


    def execute_cmd(self, cmd, params):
        driver = self.get_driver()
        resource = f"/session/{driver.session_id}/chromium/send_command_and_get_result"
        _url = driver.command_executor._url + resource
        body = json.dumps({'cmd': cmd, 'params': params})
        response = driver.command_executor._request('POST', _url, body)
        return response.get('value')
    
       
    @classmethod
    def typeTelegram(cls):
        value = cls.request.get('typeTelegram')
        return value
    
    @classmethod
    def indexStation(cls):
        value = cls.request.get('indexStation')
        if value is None:
            if cls.typeTelegram() == 'hydro':
                return ' '.join(cls.__list_station_hydro)
            else:
                return ' '.join(cls.__list_station_meteo)
        else:
            return value

    @classmethod
    def numberMessages(cls):
        value = cls.request.get('numberMessages')
        if value is None:
            return str(cls.quantity_messages())
        else:
            return value

   
    @classmethod
    def dateStartingInput(cls):
        value = cls.request.get('dateStartingInput')
        if value is None:
            return  cls.date_now
        else:
            return datetime.date.fromisoformat(value)

    @classmethod
    def dateFinishInput(cls):
        value = cls.request.get('dateFinishInput')
        if value is None:
            return (cls.date_now - datetime.timedelta(2))
        else:
            return datetime.date.fromisoformat(value)
    
    @classmethod
    def quantity_messages(cls) -> int:
        delta_date = cls.dateStartingInput() - cls.dateFinishInput()
        return delta_date.days   
     

    @classmethod
    def timeStartingInput(cls):
        value =  cls.request.get('timeStartingInput')
        if value is None:
            return cls.time_now
        else:
            return datetime.time.fromisoformat(value)


    @classmethod
    def timeFinishInput(cls):
        value = cls.request.get('timeFinishInput')
        if value is None:
            return cls.time_now
        else:
            return datetime.time.fromisoformat(value)


    @classmethod    
    def date_time_start_input(cls):
        start = cls.dateStartingInput().strftime(cls.format_spec_day) + ' ' + cls.timeStartingInput().strftime(cls.format_spec_time)
        return (datetime.datetime.strptime(start, cls.dt_fmt) + datetime.timedelta(hours=2)).strftime(cls.dt_fmt)

    @classmethod
    def date_time_finish_input(cls):
        finish = cls.dateFinishInput().strftime(cls.format_spec_day)  + ' ' + cls.timeFinishInput().strftime(cls.format_spec_time)
        return (datetime.datetime.strptime(finish, cls.dt_fmt) + datetime.timedelta(hours=-2)).strftime(cls.dt_fmt)

    @classmethod
    def input_menu(cls):
        return cls.driver.find_element(xpath, menu_gidro_xpath).click()
    
    @classmethod
    def input_menu_request(cls):
        menu_request = cls.typeTelegram()
        if menu_request == 'hydro':
            return cls.actions.click(on_element=cls.input_menu())
        else:
            pass


    @classmethod
    def element_index(cls):
        return cls.driver.find_element(xpath, index_xpath) 

    @classmethod
    def index_input(cls):
        index = cls.indexStation()
        return cls.actions.send_keys_to_element(cls.element_index(), index)            

    @classmethod                                     
    def number_of_messages(cls):
        element = cls.driver.find_element(xpath, number_of_messages_xpath)
        element.clear()
        return element    
                         
    @classmethod
    def namber_message_telegrame(cls):
        quantity = cls.numberMessages()
        return cls.actions.send_keys_to_element(cls.number_of_messages(),quantity)
       
    @classmethod
    def time_starting(cls):
        element = cls.driver.find_element(xpath, timings_starting_xpath)
        element.clear()
        return element  


    @classmethod
    def date_time_start(cls):
        date = cls.date_time_start_input()
        return cls.actions.send_keys_to_element(cls.time_starting(), date)
    
    @classmethod    
    def timings_finish(cls):
        element = cls.driver.find_element(xpath, timings_finish_xpath)
        element.clear()
        return element  


    @classmethod
    def date_time_finish(cls):
        date = cls.date_time_finish_input()
        return cls.actions.send_keys_to_element(cls.timings_finish(), date)
        
    
    @classmethod
    def post_request_element(cls):
        return cls.driver.find_element(xpath, post_request_xpath)
    
    @classmethod    
    def post_request(cls):
      return cls.actions.click(on_element=cls.post_request_element())
      

    @classmethod
    def save_html(cls):
        cls.input_menu_request()
        cls.actions.pause(1)
        cls.index_input()
        cls.actions.pause(1)
        cls.namber_message_telegrame()
        cls.date_time_start()
        cls.actions.pause(1)
        cls.date_time_finish()
        cls.actions.pause(1)
        cls.post_request()
        cls.driver = cls.get_driver()
        cls.actions.perform()
        html = cls.driver.page_source
        return SaveHtmlFile.save_html(html)

    @classmethod
    def list_logik(cls):
        list_log = [cls.save_html,
                    cls.restart_session]
        return list_log
    
    @classmethod
    def __call__(cls, **kwargs):
        cls.request = kwargs
        cls.save_html()
        cls.restart_session()
        cls.process_telegram()
        # save_report = MongoDb(cls.typeTelegram())
        # save_report.save_document()
    
    @classmethod
    def process_telegram(cls):
          # Шаг 1: парсимо HTML файл
        for report_today in SoupHtmlFile().report():
            id_teleg = report_today.id_telegrame
            date_tel = report_today.date_telegram
            time_teleg = report_today.time_telegram
            index_post = report_today.index_station
            text_telegram = report_today.gauges_telegrame
            data_telegram = {
                "id_teleg": id_teleg,
                "date_telegram": date_tel,
                "time_telegram": time_teleg,
                "index_station": index_post,
                "gauges_telegram": text_telegram}
            telegram_obj = TelegramFactory.create_telegram(cls.typeTelegram(), **data_telegram)
            if cls.typeTelegram() == 'hydro':
                decoded_telegram = telegram_obj.parse()

            else:  # 'meteo'
                decoded_telegram = telegram_obj.relative_telegam()
            document_mongo = {
            "id_telegram": id_teleg,
            "data": [data_telegram, decoded_telegram]}
            print(document_mongo)
            # collection = db.db_manager.get_or_create_collection(cls.typeTelegram())
            # db.db_manager.insert_document_if_not_exists(collection, document_mongo)
    



