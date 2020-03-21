# -*- coding: utf-8 -*-
"""
@author: Vladimir Antipov
@mail: va.antipov91@gmail.com 
"""

import yaml
import sys, getopt
import weater_requests

if __name__ == "__main__":
    help_text = ('weater.py -i <inputFile>, -c <city>, -d <distance>, -cfg <config>')

    input_file = ''
    city_name = ''
    distance = 100.0
    zoom = 10
    config_file = 'config.yaml'    
    
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:c:d:cfg:', ['inputFile=', 'city=', 'distance=', 'config='])
    except getopt.GetoptError:
        print(help_text)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(help_text)
            sys.exit()
        elif opt in ('-i', '--inputFile'):
            input_file = arg
        elif opt in ('-c', '--city'):
            city_name = arg
        elif opt in ('-d', '--distance'):
            distance = float(arg)
        elif opt in ('-cfg', '--config'):
            config_file = arg

    if not city_name and not input_file:
        print ('You did not enter a city name or files with a list of cities!')
        
    try:
        file = open(config_file)        
        config_data = yaml.safe_load(file)
        file.close()
    except IOError:
        print('Could not load config file')
        sys.exit(2)
            
    weater_cfg = weater_requests.WeaterConfig(config_data)
    requests = weater_requests.WeaterRequests(weater_cfg)
    
    cities_data = []
    if not input_file:
        cities_data.append({'name': city_name, 'distance': distance})
    else:
        try:
            file = open(input_file)
            lines = file.readlines()
            file.close()
        except IOError:
            print('Could not load file with cities')
            sys.exit(2)
        for line in lines:
            data = line.split(';')
            cities_data.append({'name': data[0], 'distance': float(data[1])})
        
    for city_data in cities_data:        
        city = requests.get_city_by_name(city_data['name'])
        cities = requests.get_cities_within_rectangle(city.lon, city.lat, city_data['distance'], zoom)
        mean_temperature = sum([city.temperature for city in cities]) / len(cities)
        print('Mean temperature in {0} is {1} in {2}'.format(city.name, mean_temperature, weater_cfg.dimension_temperature))