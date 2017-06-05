"""
Script name: lab6-2-delete-application.py
Delete a custom application
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

# Select a custom application from the list and return it's id

def select_application(ap):
    """
    This function ask user to select a custom application from a list

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    str : custom application id
    """

    app = []
    params={"isCustom":True} # filter, only retrieve custom application
    try:
        resp= ap.get(api="application",params=params) # The response (result) from "GET /application" request
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        app = response_json["response"]
    except:
        print ("Something wrong, cannot get application information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        sys.exit()

    custom_app = []
    if app != [] :   # if response is not empty
        # Extracting attributes
        idx=0
        for item in app:
            idx+=1 # adding numbers in the list
            custom_app.append([idx,item["name"],item["id"]])
        # Show all custom applications
        # Pretty print tabular data, needs 'tabulate' module

    if custom_app == []:
        print ("No custom NBAR2 application found, nothing to delete !")
        sys.exit()
    else:
        name_list=[]   # List of all custom application names
        app_in_policy=[] # list of all all custom applications which are used by policy
        for item in custom_app:
            name_list.append(item[1])
        # Iterate through all polices to find out if custom application is used
        resp= ap.get(api="policy")
        policy = resp.json()["response"]
        for item in policy:
            if "resource" in item:
                for item1 in item["resource"]["applications"]:
                    if item1["appName"] in name_list:
                        app_in_policy.append([item1["appName"],item["policyName"]])
        # Here, we check if there are applications used by policy
        # If there are applications used the we won't be able to delete
        i = 0
        policy_name_idx=2
        # Iterate custom application list
        for item in custom_app:
            match = False
            # Go Through 'in used' applications and insert policy name in the position 2 of the list
            for item1 in app_in_policy:
                print (item[1])
                if item[1] in item1:
                    match = True
                    policy_name=item1[1]
                    break
            if match:
                custom_app[i].insert(policy_name_idx,policy_name)
            else:
                custom_app[i].insert(policy_name_idx,"") # leave it blank if not used by any policy
                i=i+1
        print ("******** If application is used by policy it cannot be deleted ! *************")
        print (tabulate(custom_app, headers=['number','custom application','used by policy'],tablefmt="rst"),'\n')

    ######## Now let user to select an application and delete it #######
    # Ask user's input
    # In the loop until 'id' is assigned or user select 'exit'
    app_id = ""
    id_idx = 3 # #custom_app id is in position 3
    while True:
        user_input = input('=> Select a number for the application to delete:' )
        user_input= user_input.replace(" ","") # ignore space
        if user_input.lower() == 'exit':
            sys.exit()
        if user_input.isdigit():
            if int(user_input) in range(1,len(custom_app)+1):
                app_id = custom_app[int(user_input)-1][id_idx] #custom_app id is in position 3
                return app_id
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

#### Delete application ####

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    app_id=select_application(myapicem)  # get custom application id
    try:
        myapicem.delete(api="application/"+app_id,printOut=True) # Delete application by application id
    except:
        print ("Something wrong with deleting application")
        sys.exit()
