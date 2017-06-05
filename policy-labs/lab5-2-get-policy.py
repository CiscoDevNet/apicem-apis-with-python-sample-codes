"""
Script name: lab5-2-get-policy.py
Get all policy
"""

from apicem import *  # APIC-EM IP is assigned in apicem_config.py


def get_policy(ap):
    """
    This function print out all policies

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    None
    """

    # policy list
    policy = []
    try:
        resp= ap.get(api="policy") # The response (result) from "GET /policy" request
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        policy = response_json["response"] # network-device
    except:
        print ("Something wrong, cannot get policy information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()

    # Make sure there is at least one policy

    if policy == [] :
        print ("No policy was found !")
        sys.exit()
    # if response is not empty
    policy_list = []
    # Extracting attributes
    for item in policy:
        policy_list.append([item["policyName"],item["instanceUuid"]])
    # Show all policies
    # Pretty print tabular data, needs 'tabulate' module
    print (tabulate(policy_list, headers=['policy','id'],tablefmt="rst"),'\n')

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance, taking all defaults from apicem_config.py
    get_policy(myapicem)


