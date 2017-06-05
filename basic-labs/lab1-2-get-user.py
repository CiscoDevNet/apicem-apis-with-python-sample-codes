"""
Script name: lab1-2-get-user.py
Get all APIC-EM users with their roles
"""

from apicem import *


# Controller ip, username and password are defined in apicem_config.py
# The get() function is defined in apicem.py
# Get token function is called in get() function
try:
    resp= get(api="user")
    response_json = resp.json() # Get the json-encoded content from response
    print (json.dumps(response_json,indent=4),'\n') # Convert "response_json" object to a JSON formatted string and print it out
except:
    print ("Something wrong with GET /user request")
    sys.exit()

# Parsing raw response to list out all users and their role
for item in response_json["response"]:
    for item1 in item["authorization"]:
        print ("User \'%s\', role is the %s."%(item["username"],(item1["role"])[5:]))

# [5:] = skip first 5 characters of string item1["role"]
