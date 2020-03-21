# -*- coding: utf-8 -*-
"""
@author: Vladimir Antipov
@mail: va.antipov91@gmail.com 
"""

import requests
import wmath
import sys

class WeaterConfig():
    def __init__(self, data):
        self.__api_key = data['apiKey']
        self.__units = data['units']
        self.__cities_within_rectangle_request = data['requests']['citiesWithinRectangleZone']
        self.__by_city_name_request = data['requests']['byCityName']
        self.__dimension_temperature = self.__determine_dimension_temperature(data['units'])
        
    @property
    def api_key(self):
        """Return account API key from OpenWeatherMap"""
        return self.__api_key

    @property
    def units(self):
        """Return unit type used. Standard, metric, and imperial units are available"""
        return self.__units        
        
    @property
    def cities_within_rectangle_request(self):
        """Return cities within rectangle request uri"""
        return self.__cities_within_rectangle_request

    @property
    def by_city_name_request(self):
        """Return city name request uri """
        return self.__by_city_name_request

    @property
    def dimension_temperature(self):
        """Return used temperature dimension"""
        return self.__dimension_temperature
    
    def __determine_dimension_temperature(self, units):
        """Determines the temperature dimension with the corresponding unit type"""
        if units == 'imperial':
            return 'Fahrenheit'
        elif units == 'metric':
            return 'Celsius'
        else:
            return 'Kelvin'

class City():
    def __init__(self, json_data):
        self.id = json_data['id']
        self.name = json_data['name']
        self.lon = json_data['coord']['lon']
        self.lat = json_data['coord']['lat']
        self.temperature = json_data['main']['temp']
        
class WeaterRequests():
    def __init__(self, weater_cfg):
        self.__weater_cfg = weater_cfg

    def get_city_by_name(self, name):
        """Call current weather data by city name"""
        url = self.__weater_cfg.by_city_name_request
        params = [('q', name), ('units', self.__weater_cfg.units), ('appid', self.__weater_cfg.api_key)]
        data_response = self.__get_request(url, params)
        return City(data_response)
    
    def get_cities_within_rectangle(self, lon, lat, rectangle_side, zoom):
        """Call current weater data from cities within rectangle zone"""
        url = self.__weater_cfg.cities_within_rectangle_request
        rect = wmath.get_geographical_rect(lon, lat, 2.0 * rectangle_side)
        params = [('bbox', "{0},{1},{2},{3},{4}".format(rect[0], rect[1], rect[0] + rect[2], rect[1] + rect[3], zoom)), ('units', self.__weater_cfg.units), ('appid', self.__weater_cfg.api_key)]
        data_response = self.__get_request(url, params)
        cities = []
        for data in data_response['list']:
            cities.append(City(data))
        return cities

    def __get_request(self, url, params):
        """Call data"""
        try:
            response = requests.get(url, params = params)
            response.raise_for_status()
        except requests.exceptions.ConnectTimeout:
            print('Connection timeout occured!')
            sys.exit(2)
        except requests.exceptions.ReadTimeout:
            print('Read timeout occured')
            sys.exit(2)
        except requests.exceptions.ConnectionError:
            print('Check your internet connection')
            sys.exit(2)
        except requests.exceptions.HTTPError as e:
            print('Response is: {0}'.format(e.response.content))
            sys.exit(2)
            
        json_response = response.json()
        data = self.__lower_keys(json_response)
        return data
        
    def __lower_keys(self, x):
        """Setting a lowercase key in dictionary"""
        if isinstance(x, list):
            return [self.__lower_keys(v) for v in x]
        elif isinstance(x, dict):
            return dict((k.lower(), self.__lower_keys(v)) for k, v in x.items())
        else:
            return x