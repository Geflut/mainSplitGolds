# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 12:29:06 2024

@author: tnhannotte
"""

# from datetime import datetime
# from pytimeparse import parse


# time_str = '130::55::26'
# time_object = parse(time_str)
# print(type(time_object))
# print(time_object)

import re
from datetime import timedelta


regex = re.compile(r'((?P<hours>\d+?):)?((?P<minutes>\d+?):)?((?P<seconds>\d+?):)?((?P<milliseconds>\d+?)$)?')


def parse_time(time_str):
    parts = regex.match(time_str)
    if not parts:
        return
    parts = parts.groupdict()
    time_params = {}
    for name, param in parts.items():
        if param:
            time_params[name] = int(param)
    return timedelta(**time_params)

delta = parse_time("100:12:24:017")
delta2 = parse_time("2:15:22:051")

print(delta)
print(delta2)
print(delta + delta2)