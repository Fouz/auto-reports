import re
from psd_tools import PSDImage
# from psd_tools.api.layers import PixelLayer
from psd_tools.api.layers import Group
from datetime import date
import os, csv
import win32com.client, sys
import datetime
import metricsHandler
import lmsHandler

metrics_file = r".\data\Metrics.csv"
lms_file = r".\data\lmsIndicators.csv"

baseline = {'SAMPLE DATE': '1/13/2021', 'ENVIRONMENT': 'Production', 'ACTIVE USERS': '33688', 'AVAILABLE USERS': '33844', 'ENABLED USERS': '33985', 'TOTAL USERS': '62960', 'ENROLLMENTS': '1944698',
 'COURSES': '52470', 'ENABLED COURSES': '9531', 'LOGINS': '2194', 'ASSESSMENTS': '0', 'DISCUSSIONS': '131173', 'PLUGINS': '107', 'COURSEDOCS': '92442', 'UNIQUE ACTIVE USERS ': ''}

with open(metrics_file) as f:
  metrics_data = [{str(k): str(v) for k, v in row.items() }
    for row in csv.DictReader(f, skipinitialspace=True)]

with open(lms_file) as f:
  lms_data = [{str(k): str(v) for k, v in row.items()}
    for row in csv.DictReader(f, skipinitialspace=True)]
lms_data.remove(baseline)

def numOfDays(date1, date2):
    return (date2-date1).days


def process_date(dd):
    datetimeobject = datetime.datetime.strptime(dd, '%m/%d/%Y')
    newformat = datetimeobject.strftime('%Y-%m-%d')
    res = (datetime.datetime.strptime(newformat, '%Y-%m-%d'))
    return(str(res))

if len(sys.argv) != 3:
    print("insuficient inputs")
    exit()

date_format = '%m/%d/%Y'

try:
  start = datetime.datetime.strptime(sys.argv[1], date_format)
  to = datetime.datetime.strptime(sys.argv[2], date_format)

except ValueError:
    print("Incorrect date string format. It should be m/d/Y")
    exit()

if numOfDays(start, to ) != 4:
    print("Wrong inputs")
    exit()

metricsHandler.process_metrics_data(metrics_data,start,to) 
lmsHandler.process_data(lms_data, baseline,start, to)

print("")
week = input('تقرير الأسبوع: ')
print("\n\n")
cards = input('عدد بطاقات الدعم الفني:  \n')
print("\n")
chats = input('المحادثات الفورية: \n')
print("\n")
msgs = input('رسائل البريد الإلكتروني: \n')
print("\nGenerating report start from {0} to {1}...\n".format(sys.argv[1],sys.argv[2] ))

info_string = "{2} ملخص الأسبوع {0} من {1} إلى ".format(week.strip(), re.findall(
    r"[\d]{4}-[\d]{2}-[\d]{2}?", process_date(sys.argv[1]))[0], re.findall(
    r"[\d]{4}-[\d]{2}-[\d]{2}?", process_date(sys.argv[2]))[0])

logins_chart_list = []
logins_chart_casted = []
for item in lms_data:
      val = int(item["LOGINS"])
      logins_chart_casted.append(f'{val:,}')
      logins_chart_list.append(int(val))

attendees_chart_list = []
attendees_chart_casted = []
for item in metrics_data:
      val = int(item["Attendees"])
      attendees_chart_list.append(int(val))
      attendees_chart_casted.append(f'{val:,}')

attendeesu_chart_list = []
attendeesu_casted = []
for item in metrics_data:
      val = int(item["AttendeesUnique"])
      attendeesu_chart_list.append(int(val))
      attendeesu_casted.append(f'{val:,}')

psd = PSDImage.open('template.psd')
def manage_bars(vals, lable_name):
    highst = 2782
    lowest = 3254
    list_numbers = ["1", "2", "3", "4", "5"]
    dicty = {}
    for i in range(len(list_numbers)):
          dicty[list_numbers[i]] = vals[i]

    new_copy = {}
    sorted_values = {k: v for k, v in sorted(
        dicty.items(), reverse=True, key=lambda item: item[1])}

    diff = lowest - highst
    maxV = list(sorted_values.items())[0]
    new_copy[maxV[0]] = highst
    sorted_values.pop(next(iter(sorted_values)))

    for key, value in sorted_values.items():
        percentage = value / maxV[1]
        res = percentage * diff
        ff = lowest - res
        new_copy[key] = ff

    for i, layer in enumerate(psd):
        if type(layer) == Group:
            if layer.name == lable_name:
                for bar in layer:
                    if bar.name == "bar1":
                        bar.top = new_copy["1"]
                    if bar.name == "bar2":
                        bar.top = new_copy["2"]
                    if bar.name == "bar3":
                        bar.top = new_copy["3"]
                    if bar.name == "bar4":
                        bar.top = new_copy["4"]
                    if bar.name == "bar5":
                        bar.top = new_copy["5"]


manage_bars(logins_chart_list, "A1")
manage_bars(attendees_chart_list, "A2")
manage_bars(attendeesu_chart_list, "A3")

psd.save("tmp.psd")

psApp = win32com.client.Dispatch("Photoshop.Application")
psApp.Open(r""+str(os.path.join(sys.path[0], "tmp.psd")))
doc = psApp.Application.ActiveDocument

def bind_data():
  doc.ArtLayers["SessionInstancesLaunched"].TextItem.contents = str(metricsHandler.result['SessionInstancesLaunched'])
  doc.ArtLayers["SessionInstancesPeak"].TextItem.contents = str(metricsHandler.result['SessionInstancesPeak'])
  doc.ArtLayers["SessionTime"].TextItem.contents = str(metricsHandler.result['SessionTime'])
  doc.ArtLayers["Attendees"].TextItem.contents = str(metricsHandler.result['Attendees'])
  doc.ArtLayers["AttendeesUnique"].TextItem.contents = str(metricsHandler.result['AttendeesUnique'])
  doc.ArtLayers["AttendeesPeak"].TextItem.contents = str(metricsHandler.result['AttendeesPeak'])
  doc.ArtLayers["Recordings"].TextItem.contents = str(metricsHandler.result['Recordings'])
  doc.ArtLayers["RecordingsDuration"].TextItem.contents = str(metricsHandler.result['RecordingsDuration'])

  doc.ArtLayers["LOGINS"].TextItem.contents = str(lmsHandler.result['LOGINS'])
  doc.ArtLayers["ASSESSMENTS"].TextItem.contents = str(lmsHandler.result['ASSESSMENTS'])
  doc.ArtLayers["DISCUSSIONS"].TextItem.contents = str(lmsHandler.result['DISCUSSIONS'])
  doc.ArtLayers["COURSEDOCS"].TextItem.contents = str(lmsHandler.result['COURSEDOCS'])

  doc.ArtLayers["L1"].TextItem.contents = str(logins_chart_casted[0])
  doc.ArtLayers["L2"].TextItem.contents = str(logins_chart_casted[1])
  doc.ArtLayers["L3"].TextItem.contents = str(logins_chart_casted[2])
  doc.ArtLayers["L4"].TextItem.contents = str(logins_chart_casted[3])
  doc.ArtLayers["L5"].TextItem.contents = str(logins_chart_casted[4])

  doc.ArtLayers["AU1"].TextItem.contents = str(attendeesu_casted[0])
  doc.ArtLayers["AU2"].TextItem.contents = str(attendeesu_casted[1])
  doc.ArtLayers["AU3"].TextItem.contents = str(attendeesu_casted[2])
  doc.ArtLayers["AU4"].TextItem.contents = str(attendeesu_casted[3])
  doc.ArtLayers["AU5"].TextItem.contents = str(attendeesu_casted[4])

  doc.ArtLayers["AR1"].TextItem.contents = str(attendees_chart_casted[0])
  doc.ArtLayers["AR2"].TextItem.contents = str(attendees_chart_casted[1])
  doc.ArtLayers["AR3"].TextItem.contents = str(attendees_chart_casted[2])
  doc.ArtLayers["AR4"].TextItem.contents = str(attendees_chart_casted[3])
  doc.ArtLayers["AR5"].TextItem.contents = str(attendees_chart_casted[4])

  # info
  doc.ArtLayers["info"].TextItem.contents = str(info_string)

  #tech support info 
  doc.ArtLayers["cards"].TextItem.contents = str(cards)
  doc.ArtLayers["chats"].TextItem.contents = str(chats)
  doc.ArtLayers["msgs"].TextItem.contents = str(msgs)

bind_data()
doc.SaveAs(r""+str(os.path.join(sys.path[0], "tmp.psd")))
doc.Close()
psApp.Quit()

psd = PSDImage.open('tmp.psd')
report_title = "تقرير الأسبوع {}.jpg".format(week)
psd.composite().save(report_title)

if os.path.exists("tmp.psd"):
  os.remove("tmp.psd")

print("Done\n")
