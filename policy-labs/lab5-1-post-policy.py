"""
Script name: lab5-1-post-policy.py
Create a policy
"""

from  apicem import * # APIC-EM IP is assigned in apicem_config.py

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
    while check_name:
        policy_name = input('=> Enter policy name that you like to create: ')
        policy_name = policy_name.lstrip() # Ignore leading space
        if policy_name.lower() == 'exit':
            sys.exit()
        if policy_name == "":
            print ("Oops! Policy name cannot be NULL please try again or enter 'exit'")
        else: # Check if name is used
            check_name = False
            try:
                resp= ap.get(api="policy") # The response (result) from "GET /policy" request
                response_json = resp.json() # Get the json-encoded content from response
                policy = response_json["response"]
            except:
                print ("Something wrong, cannot get policy information")
                sys.exit()
            for item in policy:
                if policy_name == item["policyName"]:
                    print ("This policy name exists, please type in different name !")
                    check_name = True
                    break
    return policy_name


########### Ask user to select a policy Business-Relevance ##############

def select_relevance():
    """
    This function list policy business relevance for user to select
    return a list that related user's selection - [relevancy_select[?],relevancy_tag[?]]

    Parameters
    ----------
    None

    Return:
    -------
    list : [relevanceLevel,relevanceTag]
    """
    relevancy_select = [[1,'Business-Relevant'],[2,'Business-Irrelevant'],[3,'Default']]
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
    list: tag list
    """
    try:
        resp = ap.get(api="policy/tag/association")
        response_json = resp.json()
        tag = response_json["response"] # Policy tags
    except:
        print ("Something wrong with getting policy tag !")
        sys.exit()

    # If there is a policy tag, the response will show what network device is tagged
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
                        i+=1
                        # Adding number in the beginning of each row
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
    str : policy tag
    """
    tag_list= get_tag_association(ap)
    print (tabulate(tag_list, headers=['#','Policy Tag associated with','Device Name','Device IP','Deice ID'],tablefmt="rst"),'\n')

    # In the loop until tag is selected or user select 'exit'
    tag_name_idx = 1
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
    return tag_name

########## Select an application and retrieve its id #################
def select_app(ap):
    """
    This function list applications for user to select
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
        app_name = input('=> Enter application name from above(default or custom,case-sensitive) to create policy: ')
        app_name = app_name.lstrip() # Ignore leading space
        if app_name.lower() == 'exit':
            sys.exit()
        for item in app_list:
            if app_name == item[0]: # if user_input(application name) is matched
                app_id = item[1]    # index 1 is the application id
                select = False
                break
        if app_id == "":
            print ("Oops! application was not found, please try again or enter 'exit'")
    # End of while loop

    return [app_name,app_id]



if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    policy_name = enter_policy_name(myapicem) # First enter policy name
    relevance = select_relevance()
    relevanceLevel = relevance[0]
    # policy_name = policy_name + relevance[1] # append relevance abbreviation to the policy name
    tag_name = select_tag(myapicem) # select a policy tag
    app = select_app(myapicem) # select an application
    app_name = app[0]
    app_id = app[1]

    # JSON object for POST /policy
    #  "SET_PROPERTY"
    policy_json = [{
    "policyName": policy_name,
    "policyOwner": "devnetuser",
    "policyPriority": 4095,
    "resource": {
        "applications": [{
            "appName": app_name,
            "id": app_id
        }]
    },
    "actions":[
          "SET_PROPERTY"
    ],
    "policyScope": tag_name,
    "actionProperty": {
        "relevanceLevel": relevanceLevel
        }
    }]

    ########## Creating policy #############
    print ("\nCreating policy with a single application.........\n")
    try:
        myapicem.post(api="policy", data=policy_json,printOut=True)
    except:
        print ("Something wrong with POST policy")
        sys.exit()

