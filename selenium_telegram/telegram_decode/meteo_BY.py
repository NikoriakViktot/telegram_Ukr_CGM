import re
from pymetdecoder import synop as s

import requests

decoder = s.SYNOP()


def decode(telegram):
    return decoder.decode(telegram)

pattern = re.compile(r"(\d{12} AAXX \d{5} [\s\S]*?==)")

url = "https://www.ogimet.com/display_synopsc2.php"
params = {
    'lang': 'en',
    'estado': 'Bela',
    'tipo': 'ALL',
    'ord': 'REV',
    'nil': 'SI',
    'fmt': 'txt',
    'ano': '2024',
    'mes': '01',
    'day': '03',
    'hora': '02',
    'anof': '2024',
    'mesf': '01',
    'dayf': '04',
    'horaf': '02',
    'send': 'send'
}

# Виконання POST-запиту з використанням параметрів
response = requests.post(url, data=params)

# Перевірка статус-коду та виведення вмісту відповіді
if response.status_code == 200:
    matches = pattern.findall(response.text)
    data = [line.replace('\n', '').replace('==', '') for line in matches]

    data = [' '.join(line.split()) for line in data]
    # Виведення результатів
    for match in data:
        decode(match[12:])

        print(decode(match))

else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
