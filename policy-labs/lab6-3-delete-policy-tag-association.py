"""
Script name: lab6-3-delete-tag-association.py
Delete a tag association
"""

from apicem import *  # APIC-EM IP is assigned in apicem_config.py

def select_tag_association(ap):
    """
    This function ask user to select a tag association from a list

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    list :  [tag_to_delete,device_id_to_delete]
    """
    # Get policy tag association

    try:
        resp = ap.get(api="policy/tag/association")
        response_json = resp.json()
        tag = response_json["response"] # policy tag association
    except:
        print ("Something wrong with getting policy tag !")
        sys.exit()
    tag_list = []
    i=0
    for item in tag:
        if "policyTag" in item:
            if item["networkDevices"] != []:
                for item1 in item["networkDevices"]:
                    i+=1
                    tag_list.append([i,item["policyTag"],item1["deviceName"],item1["deviceIp"],item1["deviceId"]])
    if tag_list ==[]:
        print ("No policy tag association is found, nothing to delete")
        sys.exit()

    print ("The following are network devices that have policy tag")
    print (tabulate(tag_list, headers=['#','Policy Tag associated with','Device Name','Device IP'],tablefmt="rst"),'\n')


    # Ask user's input
    # In the loop until tag is selected or user select 'exit'
    tag_to_delete=""
    device_id_to_delete=""
    while True:
        tag_num = input('=> Enter a number from above to delete policy tag association: ')
        tag_num = tag_num.replace(" ","") # ignore space
        if tag_num.lower() == 'exit':
            sys.exit()
        if tag_num.isdigit():
            if int(tag_num) in range(1,len(tag_list)+1):
                tag_to_delete=tag_list[int(tag_num)-1][1]
                device_id_to_delete=tag_list[int(tag_num)-1][4]
                break
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

    if tag_to_delete=="" or device_id_to_delete=="":
        print ("For some reason, tag name is NULL!")
        sys.exit()
    else:
        return  [tag_to_delete,device_id_to_delete]

########################## Delete policy tag association ########################

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance
    tag_id_list=select_tag_association(myapicem)

    params={"policyTag":tag_id_list[0],"networkDeviceId":tag_id_list[1]}
    # To delete tag association needs to pass name of policy tag and network device id as parameters
    try:
        myapicem.delete(api="policy/tag/association/",params=params,printOut=True)
    except:
        print ("Something wrong with deleting policy/tag/association")
        sys.exit()


