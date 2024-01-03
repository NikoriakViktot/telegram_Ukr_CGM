

def f(value):
    r= value[1:].isdigit()
    if r == False:
        return {'value': value,
                'water_temperature': float(int(value[1:3]) / 10),
                'air_temperature': None, 'unit': 'Cel'}
    else:
        return {'value': value}


print(f('42111'))
