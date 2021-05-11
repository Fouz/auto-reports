import datetime
from datetime import datetime

result = {}

def process_data(data,baseline_date,  start, to):

    for item in data:
        if baseline_date in item.values():
            baseline = item
        
    try:
        data.remove(baseline)
        result["LOGINS"] = find_sum(data,"LOGINS", start = start, to = to)
        result["ASSESSMENTS"] = find_sum(data,"ASSESSMENTS", start = start, to = to)   
        result["DISCUSSIONS"] = do_the_thing(data,baseline,  "DISCUSSIONS", start=start, to=to)
        result["COURSEDOCS"] = do_the_thing(data, baseline,  "COURSEDOCS", start=start, to=to)
    except:
        print("Not a baseline date!")
        exit()
    
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
    # print(f'{res:,}')
    return(f'{res:,}')