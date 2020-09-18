#!/usr/bin/python3
"""
File: bulkPostNetObjs.py
Inputs: CSV file with network objects for a bulk import
Outputs: none

To use this file as a standalone script the username, password, & FMC IP
will need to be populated in the __main__ section below.
"""

# include the necessary modules
import argparse
import json
import requests
import textwrap

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
    # first set up the command line arguments and parse them
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.description = textwrap.dedent('''\
...         input file formatting – one name per line
...         --------------------------------
...         name,value,description,overridable,type
    ''')

    parser.add_argument("csvInput", type=str,
        help="provide the csv of network objects \
            to add.")
    args = parser.parse_args()

    # set needed variables to generate a token
    u = "apiUser"
    p = "Firepower~!"
    ip = "ip.of.fmc"
    path = "/api/fmc_platform/v1/auth/generatetoken"
    header = {} # don't need to instantiate this, but doing so for clarity
    payload = [] # don't need to instantiate this, but doing so for clarity

    # call the token generating function and populate our header
    header = get_token(ip, path, u, p)

    # we need to update our path to account for the domain UUID as follows
    path = f"/api/fmc_config/v1/domain/{header['DOMAIN_UUID']}/object/networks?bulk=true"

    # and process the file into the payload
    with open(args.csvInput) as file:
        for netObjs in file:
            netObj = netObjs.strip().split(',')
            try: # try block in case something unexpected occurs
                netObject = f'{{"name": "{netObj[0]}","value": "{netObj[1]}","overridable": {netObj[2]},"description": "{netObj[3]}","type": "{netObj[4]}"}}'
                payload.append(json.loads(netObject))

            except Exception as err:
                raise SystemExit(err)
    
    print(json.dumps(payload, indent=4))
    # now to POST our list of network objects
    try:
        r = requests.post(f"https://{ip}/{path}", headers=header, 
            data=f'{payload}', verify=False)
        

        print(r.request.body)
        print("Headers: " + str(r.headers) + "\n")
        print("Text: " + str(r.text) + "\n")
        print("Status Code: " + str(r.status_code))

    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)