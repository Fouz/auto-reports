import datetime

result = {"SessionInstancesLaunched":0,
        "SessionInstancesPeak":0,
        "SessionTime":0,
        "Attendees":0,
        "AttendeesUnique":0,
        "AttendeesPeak":0,
        "Recordings":0,
        "RecordingsDuration":0}

def process_metrics_data(data, start="",  to =""):

        result["SessionInstancesLaunched"] = find_sum(data,"SessionInstancesLaunched", start = start, to =to )
        result["Attendees"] = find_sum(data,"Attendees", start = start, to =to )
        result["AttendeesUnique"] = find_sum(data,"AttendeesUnique", start = start, to =to )
        result["Recordings"] = find_sum(data,"Recordings", start = start, to =to )
        result["SessionInstancesPeak"] = find_max(data,"SessionInstancesPeak", start = start, to =to )
        result["AttendeesPeak"] = find_max(data, "AttendeesPeak", start = start, to =to )
        result["SessionTime"] =  find_time_sum(data,"SessionTime", start = start, to =to )
        result["RecordingsDuration"] = find_time_sum(data,"RecordingsDuration", start = start, to =to )

def find_sum(data, key, start, to ):
    sum = 0
    for item in data:
        item_date = datetime.datetime.strptime(item[next(iter(item))], '%m/%d/%Y')
        if (item_date >= start):
            if (item_date <= to ):
                sum += int(item[key])
    return(f'{sum:,}')
    
def find_time_sum(data, key, start , to ):
    
    list_time = []
    for item in data:
        item_date = datetime.datetime.strptime(item[next(iter(item))], '%m/%d/%Y')
        if (item_date >= start):
            if (item_date <= to):
                list_time.append(item[key])
                duration = datetime.timedelta()
                for i in list_time:
                        (h, m, s) = i.split(':')
                        d = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
                        duration += d

    totsec = duration.total_seconds()
    h = int(totsec//3600)
    m = int((totsec % 3600) // 60)
    sec = int((totsec % 3600) % 60)

    return("{0}:{1}:{2}".format((h), m, sec))

def find_max(data, key, start, to):
    
    values = []

    for item in data:
        item_date = datetime.datetime.strptime(item[next(iter(item))], '%m/%d/%Y')
        if (item_date >= start ):
            if (item_date <= to ):
                values.append(int(item[key]))
    return(f'{max(values):,}')
