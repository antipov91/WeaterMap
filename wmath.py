# -*- coding: utf-8 -*-
"""
@author: Vladimir Antipov
@mail: va.antipov91@gmail.com 
"""

import math
   
def get_geographical_rect(lon, lat, rectangleSide):
    """Returns a rectangular area in geographic coordinates"""
    radius = 6372.8
    dLon = math.degrees(rectangleSide / (2.0 * radius))
    dLat = math.degrees(math.asin(math.sin(rectangleSide / (2.0 * radius)) / math.cos(math.radians(lon))))
    return [lon - dLon, lat - dLat, 2.0 * dLon, 2.0 * dLat]