from selenium.webdriver.common.by import By

class_by = By.CLASS_NAME
xpath = By.XPATH
menu_class = "submenu"

menu_class_xpath = '/html/body/table/tbody/tr/td[1]/a[6]'
menu_meteo_xpath = "/html/body/table/tbody/tr/td[1]/a[7]"

menu_gidro_xpath = "/html/body/table/tbody/tr/td[1]/a[10]"

list_index_class_by = "t1"
index_xpath = '/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td/input[1]'

number_of_messages_xpath = '/html/body/table/tbody/tr/td[2]/form/table/' \
                     'tbody/tr[2]/td[1]/table/tbody/tr[3]/td/font/input[1]'
timings_starting_xpath = '/html/body/table/tbody/tr/td[2]/' \
                   'form/table/tbody/tr[2]/td[1]/table' \
                   '/tbody/tr[3]/td/font/input[2]'
timings_finish_xpath = '/html/body/table/tbody/tr/td[2]/form/table' \
                 '/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/font/input[3]'
post_request_xpath = '/html/body/table/tbody/tr/td[2]/form/table/tbody/tr[1]/td/input[2]'

text_telegram_xpath = "//pre/text"
