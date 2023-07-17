
 def water_level_08(self):
        try:
            value = self.water_level_group
            match int(value[1]):
                case 0|1|2|3|4: return int(value[1:5])
                case 5: return -(int(value[2:5]))
                case 6: return -((int(value[2:5]))+1000)
                case _: return None
        except:
            return None



    def level_change(self):
        try:
            match int(self.level_change_group[4]):
                case 0: return 0
                case 1: return int(self.level_change_group[1:4])
                case 2: return -(int(self.level_change_group[1:4]))
                case _: return None
        except:
            return None



    def water_level_20_00(self):
        try:
            value = self.water_level_20_00_group
            match int(value[1]):
                case 0 | 1 | 2 | 3 | 4:
                    return int(value[1:5])
                case 5: return -(int(value[2:5]))
                case 6: return -((int(value[2:5])) + 1000)
                case _: return None
        except:
            return None



    def precipitation_day(self):
        try:
            value = self.precipitation_day_group
            match value[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value[2:4]) - 90)/10)
                case _: return float(value[1:4])

        except:
            return None


    def precipitation_day_intensity(self):
        try:
            value_precipitation_intensity = self.precipitation_day_group[4]
            if self.precipitation_day() is not None:
                match value_precipitation_intensity:
                    case '0': return '> 1'
                    case '1': return '1 - 3'
                    case '2': return '3 - 6'
                    case '3': return '6 - 12'
                    case '4': return '< 12'
                    case '/': return None
                    case _:   return None

        except:
            return None



    def precipitation_daytime(self):
        try:
            value_precipitation = self.precipitation_daytime_group[1]
            value_day = self.precipitation_daytime_group[0][3:5]
            match value_precipitation[1:4]:
                case '000': return None
                case '990'|'991'|'992'|'993'|'994'|'995'|'996'|'997'|'998'|'999':
                    return float((int(value_precipitation[2:4]) - 90)/10)
                case _: return float(value_precipitation[1:4])
        except:
            return None


    def precipitation_daytime_intensity(self):
        try:
            value_precipitation_intensity = self.precipitation_daytime_group[1][4]
            if self.precipitation_daytime() is not None:
                match value_precipitation_intensity:
                    case '0': return '> 1'
                    case '1': return '1 - 3'
                    case '2': return '3 - 6'
                    case '3': return '6 - 12'
                    case '4': return '< 12'
                    case '/': return None
                    case _:   return None


        except:
            return None



    def water_discharge(self):
        try:
            value = self.water_discharge_group
            match int(value[1]):
                case 0: return float(int(value[2:5])/1000)
                case 1: return float(int(value[2:5])/100)
                case 2: return float((int(value[2:5]))/10)
                case 3: return float(value[2:5])
                case 4: return float(int(value[2:5])*10)
                case 5: return float(int(value[2:5])*100)
                case _: return None
        except:
            return None



    def temperature_water(self):
        try:



            return float(int(self.temperature_group[1:3]))


        except:
            return self.index_gidro_station_group, None



    def temperature_air(self):
        try:
            value = self.temperature_group[3:]
            match value[3]:
                # case '/': return None
                case '5': return -(float(int(value[4])))
                case '6': return -(float(int(value[4])+10))
                case '7': return -(float(int(value[4])+20))
                case '8': return -(float(int(value[4])+30))
                case '9': return -(float(int(value[4])+40))
                case _: return float(int(value))
        except:
            return  None





  