"""
Script name: lab1-2-get-policy-tag
Get all policy tags
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def get_policy_tag(ap):
    """
    This function retrieve all policy tags

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    None
    """

    try:
        resp = ap.get(api="policy/tag",printOut=True)
    except:
        print ("Something wrong with GET /policy/tag !")

if __name__ == "__main__":
    myapicem = apicem() # Initialize apicem instance, taking all defaults from apicem_config.py
    get_policy_tag(myapicem)
