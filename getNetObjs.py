#!/usr/bin/python3
"""
File: getNetObjs.py
Inputs: none
Outputs: print a list of network objects to screen

To use this file as a standalone script the username, password, & FMC IP
will need to be populated in the __main__ section below.
"""

# include the necessary modules
import json
import requests


"""
function: get_token(fmcIP, path, username, password)
use: generates a list of necessary headers to be included with all 
    subsequent requests

inputs: IP of FMC, path to API, API user, API password
returns: access token, refresh token, domain uuid
"""
def get_token(fmcIP, path, username, password):
    # lets disable the certificate warning first (this is NOT advised in prod)
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    # send request with a try/catch block to handle errors safely
    try:
        r = requests.post(f"https://{fmcIP}/{path}", auth=(f"{username}", 
            f"{password}"), verify=False) # always verify the SSL cert in prod!
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    # return the request token
    required_headers = ('X-auth-access-token', 'X-auth-refresh-token', 'DOMAIN_UUID')
    result = {key: r.headers.get(key) for key in required_headers}
    return result








# if we're using this as a stand-alone script, run the following
if __name__ == "__main__":

    # set needed variables to generate a token
    u = "apiUser"
    p = "Firepower~!"
    ip = "ip.of.fmc:44327"
    path = "/api/fmc_platform/v1/auth/generatetoken"
    header = {} # don't need to instantiate this here, but doing so for clarity

    # call the token generating function and populate our header
    header = get_token(ip, path, u, p)

    # we need to update our path to account for the domain UUID as follows
    path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks"

    # now to try and GET our list of network objects
    try:
        r = requests.get(f"https://{ip}/{path}", headers=header, 
            verify=False) # always verify the SSL cert in prod!
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    # if it worked, we will have received a list of network objects!
    try:
        print(json.dumps(r.json(), indent=2))
    except Exception as err:
        raise SystemExit(err)