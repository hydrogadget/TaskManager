import requests
import json

SERVICE_URL="http://localhost:5000/location/"

def get_location():
  x = requests.get(SERVICE_URL)
  print json.dumps(x.json(),indent=4, sort_keys=True)

def add_new_location():
  payload = {"label":"Home","street":"5535 Hawley Ct","city":"Las Vegas","state":"NV","zip":"89118"}
  x = requests.post(SERVICE_URL,data=payload)
  print json.dumps(x.json(),indent=4, sort_keys=True)

def delete_location():
  x = requests.delete(SERVICE_URL)
  print json.dumps(x.json(),indent=4, sort_keys=True)

def update_location():
  payload = {"label":"Home","street":"9999 Hawley Ct","city":"Las Vegas","state":"NV","zip":"89118"}
  x = requests.put(SERVICE_URL,data=payload)
  print json.dumps(x.json(),indent=4, sort_keys=True)

print "Deleting location"
delete_location()

print "Adding new location"
add_new_location()

print "Dumping new location"
get_location()

print "Updating location"
update_location()

print "Dumping updated location"
get_location()
