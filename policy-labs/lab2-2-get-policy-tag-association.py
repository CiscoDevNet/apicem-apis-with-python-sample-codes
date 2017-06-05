"""
Script name: lab2-2-get-policy-tag-association.py
Tag a selected policy tag on selected network device
"""

from apicem import *  # APIC-EM IP is assigned in apicem_config.py

def get_tag_association(ap):
    """
    This function print out all network devices have policy tag
    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    None
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
                i+=1
                if item["networkDevices"] != []: # If there is at least one network device associated
                    for item1 in item["networkDevices"]: # There could be more than one network devices associated with the same tag
                        # Adding number in the beginning of each row
                        tag_list.append([i,item["policyTag"],item1["deviceName"],item1["deviceIp"],item1["deviceId"]])
                else:
                    tag_list.append([i,item["policyTag"],"","",""])
        if tag_list == []:
            print ("No policy tag association is found, nothing to show")
            sys.exit()

    print (tabulate(tag_list, headers=['#','Policy Tag associated with','Device Name','Device IP','Deice ID'],tablefmt="rst"),'\n')

if __name__ == "__main__":
    myapicem = apicem() # Initialize apicem instance, taking all defaults from apicem_config.py
    get_tag_association(myapicem)
