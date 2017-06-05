"""
Script name: lab6-1-delete-policy.py
Delete a policy
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def select_policy(ap):
    """
    This function ask user to select a policy from a list

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : [policy_name,policy_id]
    """
    policy = [] # policy list
    try:
        resp= ap.get(api="policy") # "GET /policy" request
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        policy = response_json["response"]
    except:
        print ("Something wrong, cannot get policy information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()

    # Make sure there is at least one policy
    if policy != [] :   # if response is not empty
        policy_list = []
        # Extracting attributes
        i=0
        for item in policy:
            i+=1
            policy_list.append([i,item["policyName"],item["instanceUuid"]])
        # Show all policies
        # Pretty print tabular data, needs 'tabulate' module
        print (tabulate(policy_list, headers=["#",'policy','id'],tablefmt="rst"),'\n')
    else:
        print ("No policy was found !")
        sys.exit()

    print ("!!! BUSINESS_RELEVANT_CVD_Policy,DEFAULT_CVD_Policy,BUSINESS_IRRELEVANT_CVD_Policy !!!")
    print ("!!!                  These are default policies cannot be deleted                  !!!")
    print ("--------------------------------------------------------------------------------------")

    ######## select a policy and return policy name and policy id #######
    # Ask user's input
    # In the loop until 'policy id' is assigned or user entered 'exit'

    name_idx = 1 # policy name index in the list
    id_idx = 2   # policy id index in the list
    while True:
        user_input = input('=> Select a number for the policy to delete: ' )
        user_input= user_input.replace(" ","") # ignore space
        if user_input.lower() == 'exit':
            sys.exit()
        if user_input.isdigit():
            if int(user_input) in range(1,len(policy_list)+1):
                policy_name = policy_list[int(user_input)-1][name_idx]
                policy_id = policy_list[int(user_input)-1][id_idx]
                return [policy_name,policy_id] # return value of this function
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

#### Delete Policy ####

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    policy_info=select_policy(myapicem)
    print ("Deleting",policy_info[0],"....") # policy_info[0] = policy_name
    try:
        # delete policy by policy id
        myapicem.delete(api="policy/"+policy_info[1],printOut=True) # policy_info[1] = policy_id
    except:
        print ("Something wrong with deleting policy")
        sys.exit()

