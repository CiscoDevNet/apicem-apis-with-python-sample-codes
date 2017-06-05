"""
Script name: lab3-1-post-application.py
Create an application
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def post_app(ap,app_json):
    """
    This function is used to create an application

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py
    app_json(JSON): JSON object for POST /application

    Return:
    -------
    None
    """

    ########## Get category id ##########
    # We need to know category id in the JSON of "POST /application" API
    # If the DB initialize, these ids will change. So get id dynamically.

    try:
        resp= ap.get(api="category") # The response (result) from "GET 'category" request
        response_json = resp.json() # Get the json-encoded content from response
        categories = response_json["response"] # category
    except:
        print ("Something wrong, cannot get category information")
        sys.exit()
    # Find the category id for the category name is used in JSON
    for item in categories:
        if item["name"] == app_json["category"]:
            app_json["categoryId"] = item["id"]

    # Populate user input to JSON object
    app_json["helpString"] = pApp
    app_json["name"] = pApp
    app_json["ignoreConflict"] = True

    # Important: Convert to list -- this API requires that
    app_json = [app_json]

    # POST application url
    try:
        resp = ap.post(api="application", data=app_json,printOut=True)
    except:
        print ("Something wrong with POST /application !")

##########################################################################
if __name__ == "__main__":
    # Creating JSON object for the  POST request

    app_json = {
        "trafficClass":"BULK_DATA",
        "helpString":"",
        "name":"",
        "appProtocol": "tcp/udp",
        "udpPorts": "8888",
        "tcpPorts": "8888",
        "pfrThresholdJitter":1,
        "pfrThresholdLossRate":50,
        "pfrThresholdOneWayDelay":500,
        "pfrThresholdJitterPriority":1,
        "pfrThresholdLossRatePriority":2,
        "pfrThresholdOneWayDelayPriority":3,
        "category":"other",
        "subCategory":"other",
        "categoryId":"",
        "longDescription": "custom application",
        "ignoreConflict":True
        }

    ########## Ask user to enter application name ##########
    # In the loop until input is not null or is 'exit'

    while True:
        print ("** The name only include letters, numbers, underscore and hyphen, no space between two words **")
        pApp = input('=> Enter application name that you like to create: ')
        pApp = pApp.lstrip() # Ignore leading space
        if pApp.lower() == 'exit':
            sys.exit()
        if pApp == "":
            print ("Oops! Application name cannot be NULL please try again or enter 'exit'")
        else:
            break
    # Everything is OK so far, initialize apicem instance and create application
    myapicem = apicem()
    post_app(myapicem,app_json)

