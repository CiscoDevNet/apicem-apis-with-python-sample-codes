"""
Script name: lab2-1-post-policy-tag-association.py
Tag a selected policy tag on selected network device
"""

from apicem import * # APIC-EM IP is assigned in apicem_config.py

def select_device_id(ap):
    """
    This function returns a network device id that user selected from a list.
    Exit script if there is no any network device.

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    str: network device id
    """
    device=[]
    # Create a list of network devices
    try:
        resp = ap.get(api="network-device")
        status = resp.status_code
        response_json = resp.json() # Get the json-encoded content from response
        device = response_json["response"] # The network-device
    except:
        print ("Something wrong, cannot get network device information")
        sys.exit()

    if status != 200:
        print ("Response status %s,Something wrong !"%status)
        print (resp.text)
        sys.exit()

    if device == []:
        print ("Oops! No device was found ! Discover network device first.")
        sys.exit()

    device_list = []
    # Extracting attributes and add a counter to an iterable
    idx=0
    for item in device:
        idx+=1
        device_list.append([idx,item["hostname"],item["managementIpAddress"],item["type"],item["instanceUuid"]])
    if device_list == []:
        print ("There is no network-device can be used to associate with policy tag !")
        sys.exit()
    # Pretty print tabular data, needs 'tabulate' module
    print (tabulate(device_list, headers=['number','hostname','ip','type'],tablefmt="rst"),'\n')

    # Ask user's selection
    # Find out network device with selected ip or hostname, index 4 is the network device id
    # In the loop until 'id' is assigned or user enter 'exit'
    net_id = ""
    device_id_idx = 4 # Network device ip index in the list
    while True:
        user_input = input('Select a number for the device from the list to add policy tag: ')
        user_input= user_input.lstrip() # Ignore leading space
        if user_input.lower() == 'exit':
            sys.exit()
        if user_input.isdigit(): # Make sure user's input in in range
            if int(user_input) in range(1,len(device_list)+1):
                net_id = device_list[int(user_input)-1][device_id_idx] # The device_id_idx is the position of id
                return net_id
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

######## select a policy tag to associate with device ##########

def select_policy_tag(ap):
    """
    This function returns a policy tag that user selected from a list.
    Exit script if there is no policy tag.

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py

    Return:
    -------
    str: policy tag
    """

    try:
        resp = ap.get(api="policy/tag") # get policy tag
        response_json = resp.json()
        tag = response_json["response"] # policy tags
    except:
        print ("Something wrong, cannot get host policy tag")
    if tag ==[] :
        print ("No policy tag was found, create policy tag first !")
        sys.exit()
    i=0
    tag_list = []
    for item in tag:
        i+=1
        tag_list.append([i,item["policyTag"]])
    print (tabulate(tag_list, headers=['#','Policy Tag'],tablefmt="rst"),'\n')
    pTag=""
    # Ask user's input
    # In the loop until tag is selected or user select 'exit'
    while True:
        tag_num = input('=> Select a number for the tag from the list: ')
        tag_num = tag_num.lstrip() # ignore leading space
        if tag_num.lower() == 'exit':
            sys.exit()
        if tag_num.isdigit(): # make sure digit is entered
            if int(tag_num) in range(1,len(tag)+1): # make sure digit entered is in range
                pTag=tag[int(tag_num)-1]["policyTag"]
                return pTag
            else:
                print ("Oops! number is out of range, please try again or enter 'exit'")
        else:
            print ("Oops! input is not a digit, please try again or enter 'exit'")
    # End of while loop

def post_association(ap,tag,n_id):
    """
    This function tags a selected policy tag on selected network device

    Parameters
    ----------
    ap (object): apic-em object that defined in apicem.py
    tag (str): policy tag
    n_id (str): network device id

    Return:
    -------
    None
    """

    #JSON for POST /policy/tag/association
    r_json = {
        "policyTag":tag,
        "networkDevices":[{"deviceId":n_id}]
    }
    # POST "/policy/tag/association" API
    try:
        resp = ap.post(api="policy/tag/association",data=r_json,printOut=True)
    except:
        print ("\nSomething is wrong when executing POST /policy/tag/association")

if __name__ == "__main__":
    myapicem = apicem() # initialize apicem instance, taking all defaults from apicem_config.py
    net_id = select_device_id(myapicem) # getting network device id
    tag = select_policy_tag(myapicem) # getting policy tag
    post_association(myapicem,tag,net_id) # create association


