"""
Script name: lab4-2-delete-policy-preview.py
Delete a policy
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def select_policy_preview(ap):
    """
    This function ask user to select a policy from a list

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list : [policypreview_id]
    """
    preview = [] # policy preview list
    try:
        resp= ap.get(api="policy/preview") # "GET /policy/preview" request
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        preview = response_json["response"]
    except:
        print ("Something wrong, cannot get policy information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()

    # Make sure there is at least one policy preview
    if preview != [] :   # if response is not empty
        preview_list = []
        # Extracting attributes
        i=0
        for item in preview:
            for item1 in item["policies"]:
                i+=1
                preview_list.append([i,item1["policyName"],item1["policyScope"],item["id"]])
        # Show all policy preview
        # Pretty print tabular data, needs 'tabulate' module
        print (tabulate(preview_list, headers=["#",'policy name of preview','policy scope','id'],tablefmt="rst"),'\n')
    else:
        print ("There is no policy preview, nothing to delete !")
        sys.exit()

    ######## select a policy preview and return policy preview id #######
    # Ask user's input
    # In the loop until 'policy preview id' is assigned or user entered 'exit'

    id_idx = 3   # policy preview id index in the list
    name_idx = 1
    while True:
        user_input = input('=> Select a number for the policy to delete: ' )
        user_input= user_input.lstrip() # Ignore leading space
        if user_input.lower() == 'exit':
            sys.exit()
        if user_input.isdigit():
            if int(user_input) in range(1,len(preview_list)+1):
                preview_id = preview_list[int(user_input)-1][id_idx]
                policy_name = preview_list[int(user_input)-1][name_idx]
                return [policy_name,preview_id] # return value of this function
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

#### Delete Policy ####

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    preview_info=select_policy_preview(myapicem)
    print ("Deleting",preview_info[0],"....") # preview_info[0] = policy_name
    try:
        # delete policy by policy preview id
        myapicem.delete(api="policy/preview/"+preview_info[1],printOut=True) # preview_info[1] = policy preview id
    except:
        print ("Something wrong with deleting policy")
        sys.exit()

