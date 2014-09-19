import requests
import json

SERVICE_URL="http://localhost:5000/schedules/"

def get_schedules():
  x = requests.get(SERVICE_URL)
  print json.dumps(x.json(),indent=4, sort_keys=True)

def add_new_schedule():
  payload = {"valve":"1","duration":"10","start_time":"2000","sun":"1","mon":"1","tue":"1","wed":"1","thu":"1","fri":"1","sat":"1","sun":"1"}
  x = requests.post(SERVICE_URL,data=payload)
  print json.dumps(x.json(),indent=4, sort_keys=True)


def update_schedule():
  payload = {"id":"11","valve":"2","duration":"100","start_time":"2000","sun":"1","mon":"1","tue":"1","wed":"1","thu":"1","fri":"1","sat":"1","sun":"1"}
  x = requests.put(SERVICE_URL,data=payload)
  print json.dumps(x.json(),indent=4, sort_keys=True)

def delete_schedule():
  payload = {"id":"12"}
  x = requests.delete(SERVICE_URL,data=payload)
  print json.dumps(x.json(),indent=4, sort_keys=True)


get_schedules()
add_new_schedule()

update_schedule()
delete_schedule()

get_schedules()
