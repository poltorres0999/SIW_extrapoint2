#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf8 :
'''
@author Adrià Bonet Vidal
Daily free book of Packt notifier
'''

import sys
import json
import requests

apikey = None

class Client(object):

    #Url de la web a consultar i ciutat desitjada
    location = "Lleida"
    url_base = "http://api.wunderground.com/api/"

    #Urls del servei per fer les consultes
    url_service = { 
    "hourly" : "/hourly/q/CA/",
    "almanac" : "/almanac/q/CA/",
    "conditions" : "/conditions/q/CA/"
    }


    def __init__(self, apikey):
        super(Client, self).__init__();
        self.apikey = apikey

    # Gets the weather in general (cloudy, rain) and the average humidity
    def hourly_weather(self, json_data):

        humidity = 0
        lenght = len(json_data["hourly_forecast"])
        weather = {}

        for hour in json_data["hourly_forecast"]:
            humidity = humidity + int(hour["humidity"])
            weather.setdefault(hour["condition"], 1)
            weather[hour["condition"]] = weather[hour["condition"]] +1
            
        best = 0
        for item in weather:
            con = weather[item]
            if con > best:
                best = con
                avWeather = item

        humidityAv = humidity/lenght

        return avWeather, humidityAv  

    # Obté les temperatures màximes i mínimes
    def almanac(self, json_data):

        hTemp = json_data["almanac"]["temp_high"]["normal"]["C"]
        lTemp = json_data["almanac"]["temp_low"]["normal"]["C"]

        return hTemp, lTemp

    # Obté la temperatura actual i la pressió
    def condition(self, json_data):
        
        actualT = json_data["current_observation"]["temp_c"]
        pressure = json_data["current_observation"]["pressure_mb"]

        return actualT, pressure

    def main(self):

        urlHourly = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["hourly"]) + str(self.location) + ".json"

        urlAlmanac = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["almanac"]) + str(self.location) + ".json"

        urlCond = str(self.url_base)+str(self.apikey) + \
            str(self.url_service["conditions"]) + str(self.location) + ".json"

        # Codi dedicat a obtenir la informació a partir de Json
        r = requests.get(urlHourly)
        jsonHourly = json.loads(r.text)

        r = requests.get(urlAlmanac)
        jsonAlmanac = json.loads(r.text)
 
        r = requests.get(urlCond)
        jsonCond = json.loads(r.text)


        cond, humidity = self.hourly_weather(jsonHourly)
        hTemp, lTemp = self.almanac(jsonAlmanac)
        actualT, pressure = self.condition(jsonCond)

        print "\nEl temps avui: "+ cond
        print "Temperatura " + str(actualT) +"ºC"
        print "Les temperatures màximes i mínimes " \
            +str(hTemp)+"ºC and "+str(lTemp)+"ºC"
        print "Humitat "+ str(humidity)+"%"

        print ""
        if int(actualT) <= 20:
            print "Agafa la jaqueta!"
        elif int(actualT) > 20 and int(actualT) <= 30:
            print "Farà un dia temperat, no fa falta agafar la jaqueta"
        elif int(actualT) > 30:
            print "Si pots anar despullat, millor que millor"

        if cond == "Clear" or "Cloudy" in cond.split(" "):
            if int(pressure) < 1020:
                print "El temps està estable però nubolat, hi ha opcions de pluja, agafa el paraigues"
            if int(pressure) > 1020:
                print "Farà un bon dia, no fa falta que agafis paraigues!"
        elif "Rain" in cond.split(" "):
            print "Avui plourà, agafa un paraigues!"
        else: 
            print "Farà un temps normal, no cal que et tapis"

        print "\n"

if __name__ == "__main__":

    if not apikey:
        try:
            apikey = sys.argv[1]
        except IndexError:
            print "You have to give an argument with an API key"

    weatherClient = Client(apikey)
    weatherClient.main()