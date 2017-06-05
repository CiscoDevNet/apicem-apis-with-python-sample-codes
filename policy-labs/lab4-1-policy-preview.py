"""
Script name: lab4-1-policy-preview.py
Create a policy
"""

from  apicem import * # APIC-EM IP is assigned in apicem_config.py
import time # Need it for delay - sleep() function

########### Ask user to enter a policy name ##############
# In the loop until input is not null or is 'exit'
def enter_policy_name(ap):
    """
    This function takes user input as policy name and check if the name is used
    If name is not used return user's input

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    str : policy name
    """
    check_name = True
    p_name=""
    while check_name:
        p_name = input('=> Enter the policy name that you like to create for preview: ')
        p_name = p_name.lstrip() # Ignore leading space
        if p_name.lower() == 'exit':
            sys.exit()
        if p_name == "":
            print ("Oops! Policy name cannot be NULL please try again or enter 'exit'")
        else: # Check if name is used
            check_name = False
            try:
                resp= ap.get(api="policy") # The response (result) from "GET /policy/" request
                response_json = resp.json() # Get the json-encoded content from response
                policy = response_json["response"]
            except:
                print ("Something wrong, cannot get policy information")
                sys.exit()
            for item in policy:
                if p_name == item["policyName"]:
                    print ("This policy name exists, please type in different name !")
                    check_name = True
                    break
    return p_name

########### Ask user to select a policy Business-Relevance ##############

def select_relevance():
    """
    This function list policy business relevance for user to select
    return a list that related to user's selection - [relevancy_select[?],relevancy_tag[?]]

    Parameters
    ----------
    None

    Return:
    -------
    list : [relevanceLevel,relevanceTag]
    """
    relevancy_select = [[1,"Business-Relevant"],[2,"Business-Irrelevant"],[3,"Default"]]
    relevancy_tag = ['-BR','-IR','-D']
    print (tabulate(relevancy_select, headers=['#','Policy Business Relevancy'],tablefmt="rst"),'\n')

    relevanceLevel = 'Default'
    # In the loop until tag is selected or user select 'exit'
    while True:
        tag_num = input('=> Enter a number above for policy Business Relevancy: ')
        tag_num = tag_num.lstrip() # Ignore leading space
        if tag_num.lower() == 'exit':
            sys.exit()
        if tag_num.isdigit():
            if int(tag_num) in range(1,len(relevancy_select)+1):
                relevanceTag = relevancy_tag[int(tag_num)-1]
                relevanceLevel = relevancy_select[int(tag_num)-1][1]
                break
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

    return [relevanceLevel,relevanceTag]


def get_tag_association(ap):
    """
    This function print out all network devices have policy tag
    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : tag association list
    """
    try:
        resp = ap.get(api="policy/tag/association")
        response_json = resp.json()
        tag = response_json["response"] # Policy tags
    except:
        print ("Something wrong with getting policy tag !")
        sys.exit()

    # If there is any policy tag, the response will show what network device is tagged
    if tag ==[]:
        print ("No Policy tag is found")
        sys.exit()
    else:
        tag_list = []
        i=0
        for item in tag:
            if "policyTag" in item:
                if item["networkDevices"] != []: # If there is at least one network device associated
                    for item1 in item["networkDevices"]: # There could be more than one network device associated with the same tag
                        # i - Adding number in the beginning of each row
                        i+=1
                        tag_list.append([i,item["policyTag"],item1["deviceName"],item1["deviceIp"],item1["deviceId"]])
                else:
                    i+=1
                    tag_list.append([i,item["policyTag"],"","",""])
        if tag_list == []:
            print ("No policy tag association is found, nothing to show")
            sys.exit()
    return (tag_list)

########### Ask user to select a policy tag name ##############

def select_tag(ap):
    """
    This function let user to select a policy tag

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : [tag_name,nd_id]
    """
    tag_list= get_tag_association(ap)
    print (tabulate(tag_list, headers=['#','Policy Tag associated with','Device Name','Device IP','Deice ID'],tablefmt="rst"),'\n')

    # In the loop until tag is selected or user select 'exit'
    tag_name_idx=1
    nd_id_idx = 4
    while True:
        tag_num = input('=> Select a policy tag that is associated with network device : ')
        tag_num = tag_num.lstrip() # Ignore leading space
        if tag_num.lower() == 'exit':
            sys.exit()
        if tag_num.isdigit():
            if int(tag_num) in range(1,len(tag_list)+1):
                nd_id = tag_list[int(tag_num)-1][nd_id_idx]
                if nd_id == "":
                    print ("Oops! This policy tag is not associated with any network device, please try again or enter 'exit'")
                else:
                    tag_name = tag_list[int(tag_num)-1][tag_name_idx]
                    break
            else:
                print ("Oops! Number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! Input is not a digit, please try again or enter 'exit'")
    # End of while loop
    return [tag_name,nd_id]

########## Select an application and retrieve its id #################
def select_app(ap):
    """
    This function list all applications for user to select
    return a list with application name and application id

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : [app_name,app_id]
    """

    print ("** Retrieving applications may take a while, please wait......... **\n")
    app = []
    try:
        resp= ap.get(api="application") # The response (result) from "GET /application" request
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
        print ("Something wrong for retrieving applications!")
        sys.exit()

    app_list = []
    # Extracting attributes
    for item in app:
         app_list.append([item["name"],item["instanceUuid"]])
    # Show all NBAR2 applications
    # Pretty print tabular data, needs 'tabulate' module

    print ("-------------  All default applications -------------")
    print (tabulate(app_list, headers=['application','id'],tablefmt="rst"),'\n')

    app = []
    params={"isCustom":True}
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

    # Make sure there is at least one custom application
    if app == []:
        print ("** There is no custom application, select one from default ! **\n")
    else:
        short_list = []
        # Extracting attributes
        for item in app:
            short_list.append([item["name"],item["instanceUuid"]])
        print ("*************  All custom applications *************")
        print (tabulate(short_list, headers=['custom application','id'],tablefmt="rst"),'\n')

    # Ask user's select application in order to retrieve its id
    # In the loop until 'id' is assigned or user select 'exit'

    app_id = ""
    select = True
    while select:
        app_name = input('\n=> Enter application name from above(default or custom,case-sensitive) to create policy: ')
        app_name = app_name.lstrip() # Ignore leading space
        if app_name.lower() == 'exit':
            sys.exit()
        for item in app_list:
            if app_name == item[0]: # If user_input(application name) is matched
                app_id = item[1]    # Index 1 is the application id
                select = False
                break
        if app_id == "":
            print ("Oops! application was not found, please try again or enter 'exit'")
    # End of while loop

    return [app_name,app_id]

def get_file_with_id(ap,id):
    """
    This function print out content of file

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py
    id (str): file id

    Return:
    -------
    str: file content
    """


    try:
        resp=ap.get(api="file/"+id) # The response (result) from "GET /file/{id}" request
        status = resp.status_code
        # print (resp.text)
    except:
        print ("Something wrong, cannot get file information")
        sys.exit()

    if status != 200:
        print ("Response status :",status)
        print (resp.text)
        sys.exit()

    return  resp.text

if __name__ == "__main__":
    myapicem = apicem() # Initialize apicem instance
    policy_name = enter_policy_name(myapicem) # Policy name for preview from user's input
    relevance = select_relevance()
    relevanceLevel = relevance[0]
    tag = select_tag(myapicem) # Select a policy tag scope
    tag_name = tag[0]
    net_id = tag[1]
    app = select_app(myapicem) # Select an application
    app_name = app[0]
    app_id = app[1]

    # JSON object for POST /policy/preview

    preview_json = {
        "policies":[
             {
             "policyName": policy_name,
             "policyOwner": "admin",
             "policyPriority": 4095,
             "resource": {
                 "applications": [{"appName": app_name,"id": app_id}]
              },
              "actions":["SET_PROPERTY"],
              "policyScope": tag_name,
              "actionProperty": {"relevanceLevel": relevanceLevel}
             }
         ],
         "networkDeviceIds": [
              net_id
         ],
        "state": "ENABLE_DEVICE"
    }

    ########## Creating policy preview #############
    params={"policyScope" : tag_name}
    try:
        myapicem.post(api="policy/preview", params=params,data=preview_json,printOut=True)
    except:
        print ("Something wrong with POST policy/preview")
        sys.exit()
    print ("Generating policy preview, please wait.....")
    time.sleep(2) # It take a little time to generate preview so wait couple of seconds here.
    count = 0
    preview_created = False
    loop = True
    while loop:
        time.sleep(1)
        count += 1
        print ("Generating policy preview, please wait.....")
        try:
            # Preview for this policyScope
            resp=myapicem.get(api="policy/preview",params=params,printOut = True)
            response_json = resp.json()
            preview = response_json["response"] # Policy tags
        except:
            print ("Something wrong with GET policy preview")
            sys.exit()
        if preview == []:
            print ("Something wrong with POST policy/preview, preview is not created")
            sys.exit()
        for item in preview: # Entire response from GET policy/preview
            for item1 in item["policies"]:
                if item1["policyName"] == policy_name: # Make sure preview is created, won't see the policy name if it's not created
                    preview_created = True
                    if item["deviceConfigs"] != []:
                        for item2 in item["deviceConfigs"]:
                            if item2["status"] == "FAILURE":
                                print ("*** Dry-Run Failed to Generate CLIs ***")
                                print (item2["failureReason"])
                                print ("Not thing to preview so deleting this request .....")
                                # Since nothing to view so delete this preview
                                myapicem.delete(api="policy/preview/"+item["id"])
                                sys.exit()
                            if item2["status"] == "SUCCESS":
                                file_id = (item2["fileId"])[13:] # Skip "/api/v1/file/"
                                loop = False
                                break
                            if count > 30: # Timeout after ~ 30 seconds
                                loop = False
                                if "fileId" in item2 : # The fileId may not show immediately
                                    print ("Warning: May only have partial preview content !")
                                    file_id = (item2["fileId"])[13:] # Skip "/api/v1/file/"
                                    break
                                else:
                                # Since nothing to view so delete this preview
                                    print ("\nScript time out, it takes to long to get the file id !")
                                    myapicem.delete(api="policy/preview/"+item["id"])
                                    sys.exit()
                    else:
                        if count > 30: # Timeout after ~ 30 seconds
                            loop = False
                            print ("\nScript time out, it takes to long to get the file id !")
                            myapicem.delete(api="policy/preview/"+item["id"])
                            sys.exit()

        if not preview_created: # Policy name is not found in all existing policy preview, preview is not created
            print ( "Policy preview is not created, a preview may already exist for this policy scope - ",tag_name)
            sys.exit()
    content = get_file_with_id(myapicem,file_id)
    print ("---------------- Policy Preview -----------------")
    print (content)
    print ("\nDeleting policy preview after presenting content.........\n")
    myapicem.delete(api="policy/preview/"+item["id"])
