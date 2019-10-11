'''
Copyright (c) 2019 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). A copy of the License
can be found in the LICENSE.TXT file of this software or at
https://developer.cisco.com/site/license/cisco-sample-code-license/
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
express or implied.
'''

import json
import requests


def get_smart_licenses(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a smart licenses GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: smart licenses
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    smart_licenses = None
    smart_license_url = 'api/fdm/latest/license/smartlicenses'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=smart_license_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET smart license response {} {}".format(response.status_code, response.json()))
    else:
        smart_licenses = response.json().get('items')
        for smart_license in smart_licenses:
            print('smart license found: {}'.format(str(smart_license)))
    return smart_licenses


def post_smart_license(host, port, access_token, smart_license):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a smart license POST request
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param smart_license: the smart license to be created
    :return: True if successful, otherwise False
    """
    result = True
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    smart_license_url = 'api/fdm/latest/license/smartlicenses'
    response = requests.post(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=smart_license_url),
        data=json.dumps(smart_license), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed POST smart license response {} {}".format(response.status_code, response.json()))
        result = False
    elif response.status_code == 200:
        print(response.json())
    return result
