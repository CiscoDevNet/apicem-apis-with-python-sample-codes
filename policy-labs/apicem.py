"""
This script provides the same functions as in previous leaning labs but using Python class.
This file is only used for policy labs, do not use for other labs
"""

import requests   # We use Python external "requests" module to do HTTP query
import json
import sys

# All APIC-EM configuration is in apicem_config.py
import apicem_config  # APIC-EM IP is assigned in apicem_config.py
from tabulate import tabulate # Pretty-print tabular data in Python

requests.packages.urllib3.disable_warnings() # Disable warning message
# It's used to get rid of certificate warning messages when using Python 3.
# For more information please refer to: https://urllib3.readthedocs.org/en/latest/security.html

class apicem(object):
    """ An object to provide easy RESTful request for APIC-EM APIs"""

    def __init__(self, host = apicem_config.APICEM_IP,username = apicem_config.USERNAME,
                 password = apicem_config.PASSWORD,version= apicem_config.VERSION,**kwargs):
        """      --apicem object initializer--

        When a class defines an special __init__() method,
        class instantiation automatically invokes __init__() for the newly-created class instance.

        Taking apic-em IP, login, password and version number from apicem_config.py as default
        To overwrite enter IP,username and password when initialize the instance

        Parameters
        ----------
        self: a reference to the class instance
        host (str): apic-em routable DNS address or ip
        username (str): user name to authenticate with
        password (str): password to authenticate with
        version (str): apic-em version
        **kwargs: arbitrary number of keyword arguments (optional, use as needed)

        Will use default value from apicem_config.py for host, username, password and version
        if there are not assigned during creating apicem instance.

        Methods:
        ----------
        get_X_auth_token: get token
        get_url: get the complete url i.e. 'https://myapicem.mycompany.com/api/v1/<api>'
        get: simplify requests.get
        post: simplify requests.post
        put: simplify requests.put
        delete: simplify requests.delete
        prettyPrint: pretty print raw response

        Note:
        -----
        port number can be configured in apicem_config.py as part of 'apicem_ip' string

        """

        self.__dict__.update(kwargs)
        self.api_url = "https://%s/api/%s/%s" # host, version and api
        self.host = host
        self.version = version
        self.username = username
        self.password = password
        self.headers = {"content-type":"application/json"}

        # Get authentication when initializing instant, also add token into the self.headers
        # So in get,post,put and delete methods don't need to get service ticket again
        if self.username is not None:
            self.get_X_auth_token()
        else:
            print ("need to provide username")

    def get_X_auth_token(self):
        """
        This function returns a new service ticket.
        In this function we also assign header value which is used in the get/post/put/delete functions

        Return:
        ----------
        str: APIC-EM authentication token
        """
        # All APIC-EM REST API query and response content type is JSON
        # JSON input for the post ticket API request

        r_json = {"username": self.username,"password": self.password}

        # Post ticket API request
        try:
            r = requests.post(self.get_url("ticket"),json.dumps(r_json),headers=self.headers,verify = False)
            response_json = r.json()

            # Adding 'X-Auth-Token' to header
            self.headers['X-Auth-Token'] = response_json["response"]["serviceTicket"]
            return (response_json["response"]["serviceTicket"])
        except:
            # Something wrong, cannot get service ticket
            print ("Status: %s"%r.status_code)
            print ("Response: %s"%r.text)
            sys.exit ()


    def get_url(self, api):
        """
        get the complete url path for the request

        Parameters
        ----------
        api (str): APIC-EM API

        Return:
        str: url for REST request
        """

        complete_url = self.api_url % (self.host, self.version, api)
        return complete_url

    def get(self, api, params='', printOut=False):
        """
        To simplify requests.get with default configuration.Return is the same as requests.get

        Parameters
        ----------
        api (str): api without prefix
                   example: for https://10.10.10.10/api/v1/host just use "host"
        params (str): optional parameters for the GET request
        printOut (boolean): to pretty print raw response (set True to print)

        Return:
        -------
        object: an instance of the Response object(of requests module)

        Authentication token is obtained during the object initialization and assigned to self.headers
        when calling get_X_auth_token()
        """
        try:
            url = self.get_url(api)
            print ("\nExecuting GET '%s'\n"%url)
            r = requests.get(url,headers=self.headers,params=params, verify = False)
            print ("GET '%s' Status: "%api,r.status_code,'\n') # This is the http request status
            if printOut:
                self.prettyPrint("Response:\n", r)
            return r
        except:
            print ("Something wrong to GET /",api)
            sys.exit()

    def post(self,api,data=None,params='',printOut=False):
        """
        To simplify requests.post with default configuration. Return is the same as requests.post

        Parameters
        ----------
        api (str): api without prefix
             example: for https://10.10.10.10/api/v1/policy just use "policy"
        data (JSON): JSON object for the POST request
        printOut (boolean): to pretty print raw response (set True to print)

        Return:
        -------
        object: an instance of the Response object(of requests module)

        Authentication token is obtained during the object initialization and assigned to self.headers
        when calling get_X_auth_token()
        """

        try:
            url = self.get_url(api)
            print ("\nExecuting POST '%s'\n"%url)
            r = requests.post(url, json.dumps(data), headers=self.headers,params=params,verify = False)
            print ("POST '%s' Status: "%api,r.status_code,'\n') # This is the http request status
            if printOut:
                self.prettyPrint("Response:\n", r)
            return r
        except:
            print ("Something wrong to POST /",api)
            sys.exit()


    def put(self, api, data=None, printOut=False):
        """
        To simplify requests.post with default configuration. Return is the same as requests.put

        Parameters
        ----------
        api (str): api without prefix
             example: for https://10.10.10.10/api/v1/policy just use "policy"
        data (JSON): JSON object for the POST request
        printOut (boolean): to pretty print raw response (set True to print)

        Return:
        -------
        object: an instance of the Response object(of requests module)

        Authentication token is obtained during the object initialization and assigned to self.headers
        when calling get_X_auth_token()
        """

        try:
            url = self.get_url(api)
            print ("\nExecuting PUT '%s'\n"%url)
            r = requests.put(url, data, headers=self.headers,verify = False)
            print ("PUT '%s' Status: "%api,r.status_code,'\n') # This is the http request status
            if printOut:
                self.prettyPrint("Response:\n", r)
            return r
        except:
            print ("Something wrong to PUT /",api)
            sys.exit()

    def delete(self, api, params='',printOut=False):
        """
        To simplify requests.get with default configuration.Return is the same as requests.delete
        Parameters
        ----------
        api (str): api without prefix
             example: for https://10.10.10.10/api/v1/policy just use "policy"
        params (str): optional parameters for the GET request
        printOut (boolean): to pretty print raw response (set True to print)

        Return:
        -------
        object: an instance of the Response object(of requests module)

        Authentication token is obtained during the object initialization and assigned to self.headers
        when calling get_X_auth_token()
        """
        try:
            url = self.get_url(api)
            print ("\nExecuting DELETE '%s'\n"%url)
            r = requests.delete(url, headers=self.headers, params=params, verify = False)
            print ("DELETE '%s' Status: "%api,r.status_code,'\n') # This is the http request status
            if printOut:
                self.prettyPrint("Response:\n", r)
            return r
        except:
            print ("Something wrong to DELETE /",api)
            sys.exit()

    def prettyPrint(self,text="",json_object=None):
        """
        Parameters
        ----------
        text (str) : message to print out
        json_object (Response object): an instance of the Response object(of requests module)

        Return:
        -------
        None
        """
        resp = json_object.json() # Get the json-encoded content from response
        print (text,json.dumps(resp,indent=4))    # This is the entire response from the query






