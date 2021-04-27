import numpy as np
from datetime import date, timedelta
import datetime
import re 

baseline = {'SAMPLE DATE': '1/13/2021', 'ENVIRONMENT': 'Production', 'ACTIVE USERS': '33688', 'AVAILABLE USERS': '33844', 'ENABLED USERS': '33985', 'TOTAL USERS': '62960', 'ENROLLMENTS': '1944698',
            'COURSES': '52470', 'ENABLED COURSES': '9531', 'LOGINS': '2194', 'ASSESSMENTS': '0', 'DISCUSSIONS': '131173', 'PLUGINS': '107', 'COURSEDOCS': '92442', 'UNIQUE ACTIVE USERS ': ''}


start = baseline[next(iter(baseline))]
def process_date(dd):    
    datetimeobject = datetime.datetime.strptime(dd, '%m/%d/%Y')
    newformat = datetimeobject.strftime('%Y-%m-%d')
    res = (datetime.datetime.strptime(newformat, '%Y-%m-%d'))
    return(str(res))

print(re.findall(r"[\d]{4}-[\d]{2}-[\d]{2}?", process_date(start))[0])
