import os
from requests_html import HTML

class SaveHtmlFile:
    data_html = f'data.html'
    html_obj = None

    @classmethod
    def get_html_obj(cls, html):
        if cls.html_obj is None:
            html_str = html
            cls.html_obj = HTML(html=html_str)
        return cls.html_obj

    @classmethod
    def save_html(cls, html):
        with open(cls.data_html, "w", encoding='koi8-u') as file:
            data_html = file.write(html)
            return data_html

    @classmethod
    def open_html_file(cls):
        with open(cls.data_html, 'r', encoding='koi8-u') as file:
            read_file = file.read()
            return read_file

    @classmethod
    def remove_html_file(cls):
        os.remove(cls.data_html)
