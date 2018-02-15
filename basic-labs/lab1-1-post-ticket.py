"""
This script retrieves an authentication token from APIC-EM and prints out it's value
It is standalone, there is no dependency.
"""

import requests   # We use Python "requests" module to do HTTP GET query
import json       # Import JSON encoder and decode module

requests.packages.urllib3.disable_warnings() # Disable warnings

# APIC-EM IP, modify these parameters if you are using your own APIC-EM
apicem_ip = "sandboxapicem.cisco.com"
username = "devnetuser"
password = "Cisco123!"
version = "v1"

# JSONhttps://sandboxapic.cisco.com/ input
r_json = {
    "username": username,
    "password": password
}

# POST ticket API URL
post_url = "https://"+apicem_ip+"/api/"+version+"/ticket"

# All APIC-EM REST API request and response content type is JSON.
headers = {'content-type': 'application/json'}

# Make request and get response - "resp" is the response of this request
resp = requests.post(post_url, json.dumps(r_json), headers=headers,verify=False)
print ("Request Status: ",resp.status_code)

# Get the json-encoded content from response
response_json = resp.json()
print ("\nRaw response from POST ticket request:\n",resp.text)
# Not that easy to read the raw response, so try the formatted print out

# Pretty print the raw response
print ("\nPretty print response:\n",json.dumps(response_json,indent=4))


