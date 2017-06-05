from apicem import *  # APIC-EM IP is assigned in apicem_config.py
"""
Script name: lab3-2-get-custom-application.py
Get application(s) based on the filter - "isCustom":True
"""


def get_custom_app(ap):
    """
    This function print out all network devices have policy tag
    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : A list of custom application with name and id
    """

    app = []
    # Set "isCustom = True" so the API will return only custom application(s)
    params={"isCustom":True}
    try:
        resp= ap.get(api="application",params=params) # The response from "GET /application" request
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        app = response_json["response"]
    except:
        print ("Something wrong, cannot get application information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        sys.exit()

    # Make sure there is at least one application
    if app == []:
        print ("There is no custom application !")
        sys.exit()

    app_list = []
    # Extracting attributes
    for item in app:
        app_list.append([item["name"],item["instanceUuid"]])
    # Return a list of custom application with name and id
    return app_list

if __name__ == "__main__":
    myapicem = apicem() # Initialize apicem instance
    a_list = get_custom_app(myapicem)
    if a_list !=[]:
        print ("*************  All custom applications *************\n")
        print (tabulate(a_list, headers=['custom application','application id'],tablefmt="rst"),'\n')
    else:
        print ("*************  There is no custom applications ! *************\n")

