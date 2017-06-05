"""
Script name: lab6-4-delete-policy-tag.py
Delete a policy-tag
"""

from  apicem import * # APIC-EM IP is assigned in apicem_config.py
def select_tag(ap):
    """
    This function ask user to select a policy tag a list

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    str : policy tag
    """
    try:
        resp = ap.get(api="policy/tag/count")
        response_json = resp.json()
        count = response_json["response"] # policy tags
    except:
        print ("Something wrong with getting policy tag count!")
        sys.exit()
    if count == 0 :
        print ("No policy tag is found, nothing to delete !")
        sys.exit()
    try:
        resp = ap.get(api="policy/tag/association")
        response_json = resp.json()
        tag = response_json["response"] # policy tag association
    except:
        print ("Something wrong with GET policy/tag/association!")
        sys.exit()

    tag_list = []

    i=0
    for item in tag:
        if "policyTag" in item:
            if item["networkDevices"] == []:
                i+=1
                tag_list.append([i,item["policyTag"],"",""])
            else:
                for item1 in item["networkDevices"]:
                    i+=1
                    tag_list.append([i,item["policyTag"],item1["deviceName"],item1["deviceIp"]])


    print ("*** If policy tag is associated with network device, it cannot be deleted ***\n")
    print ("---------------- Select one with no network device attached -----------------\n")
    print (tabulate(tag_list, headers=['Number','Policy Tag associated with','Device Name','Device IP'],tablefmt="rst"),'\n')

    # Ask user's input
    # In the loop until tag is selected or user select 'exit'
    tag_to_delete=""
    tag_idx = 1 # 1 is the position of policy tag
    device_ip_idx = 3 #3 is the position of device IP
    while True:
        tag_num = input('=> Enter a number from above to delete policy tag: ')
        tag_num = tag_num.replace(" ","") # ignore space
        if tag_num.lower() == 'exit':
            sys.exit()
        if tag_num.isdigit():
            if int(tag_num) in range(1,len(tag_list)+1):
                tag_to_delete=tag_list[int(tag_num)-1][tag_idx] # 1 is the position of policy tag
                # to prevent user executing `DELETE /policy/tag` API not knowing actually fail to delete policy tag
                if tag_list[int(tag_num)-1][device_ip_idx] !="":
                    print("This tag is still associated with network device, select one with no network device attached !")
                else:
                    return tag_to_delete # OK to return policy tag name
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

    if tag_to_delete=="":
        print ("For some reason, tag name is NULL!")
        sys.exit()

############################### Delete policy tag  ##############################

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    tag_to_delete = select_tag(myapicem) # get the policy tag name
    params={'policyTag':tag_to_delete} # to delete policy tag we need to pass tag name as parameter
    try:
        myapicem.delete(api="policy/tag/",params=params,printOut=True)
    except:
        print ("Something wrong with deleting policy/tag")
        sys.exit()

