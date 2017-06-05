"""
Script name: lab1-1-post-policy-tag
Create a policy tag
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def create_policy_tag(ap,tag_json):
    """
    This function is used to create a policy tag

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py
    tag_json(JSON): JSON object for POST /policy/tag

    Return:
    -------
    None
    """
    try:
        resp = ap.post(api="policy/tag", data=tag_json,printOut=True)
    except:
        print ("Something wrong with POST /policy/tag !")

if __name__ == "__main__": # Execute only if run as a script

    myapicem = apicem() # Initialize apicem instance, taking all defaults from apicem_config.py

    # Ask user's input
    # In the loop until input is not null or is 'exit'
    print ("** Tag must only include letters, numbers, underscore and hyphen, no space between two words **")
    while True:
        pTag = input('=> Enter policy tag name that you like to create: ')
        pTag = pTag.lstrip() # Ignore leading space
        if pTag.lower() == 'exit':
            sys.exit()
        if pTag == "":
            print ("Oops! Policy tag name cannot be NULL please try again or enter 'exit'")
        else:
            break

    # JSON for "POST policy/tag" request, taking user's input as tag name
    tag_json = {
        "policyTag": pTag
    }

    create_policy_tag(myapicem,tag_json) # Create tag function



