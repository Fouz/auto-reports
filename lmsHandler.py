import pandas as pd
import csv
import ast
import datetime
from datetime import datetime
import re
import sys
from collections import OrderedDict

result = {"LOGINS":0,
    "ASSESSMENTS":0,
    "DISCUSSIONS":0,
    "COURSEDOCS":0}

def process_data(data,baseline,  start, to):

    result["LOGINS"] = find_sum(data,"LOGINS", start = start, to = to)
    result["ASSESSMENTS"] = find_sum(data,"ASSESSMENTS", start = start, to = to)
    result["DISCUSSIONS"] = do_the_thing(data,baseline,  "DISCUSSIONS", start=start, to=to)
    result["COURSEDOCS"] = do_the_thing(data, baseline,  "COURSEDOCS", start=start, to=to)

def find_sum(data , key, start, to ):
    sum = 0 
    for item in data:
        item_date = datetime.strptime(item[next(iter(item))], '%m/%d/%Y')
        if (item_date >= start ) :
            if (item_date <= to ):
                if item[key] != "":
                    sum += int(float(item[key]))
             
    return(f'{sum:,}')

def do_the_thing(data, baseline, key, start, to):

    dataList = []
    for item in data:
        item_date = datetime.strptime(item[next(iter(item))], '%m/%d/%Y')
        if (item_date >= start ):
            if (item_date <= to ):
                dataList.append(int(item[key]))

    max_value = max(dataList) 
    base_line = int(baseline[key])
    res = (max_value - base_line)
    return(f'{res:,}')
