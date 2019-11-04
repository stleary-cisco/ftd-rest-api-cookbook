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

import requests


def get_intf_object(host, port, access_token, intf_hw_name):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an intrusion rule GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param intf_hw_name: hardware name of the interface which is going to be enabled for PPPoE
    :return: interface object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intf_object = None
    intf_url = 'api/fdm/latest/devices/default/interfaces'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intf_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET interface list {} {}".format(response.status_code, response.json()))
    else:
        for intf in response.json().get('items'):
            if intf['hardwareName'] == intf_hw_name:
                response = requests.get(
                    'https://{host}:{port}/{url}/{id}'.format(host=host, port=port, url=intf_url, id=intf['id']),
                    verify=False, headers=headers)
                if response.status_code != 200:
                    print('Failed GET interface {} {}'.format(response.status_code, response.json()))
                    return
                else:
                    intf_object = response.json()
                break
        else:
            print("Failed to find interface with the hardwareName: {}".format(intf_hw_name))
    return intf_object



