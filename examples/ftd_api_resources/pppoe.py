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


def update_intf_to_pppoe(host, port, access_token, intf_object, pppoe, ip_addr=''):
    """
    Requires Python v3.0 or greater and requests lib.
    Update an interface
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param intf_object: interface object
    :param pppoe: pppoe object
    :param ip_addr: if an ip address is supplied it will be set to the interface (as PPPoE static IP Address) otherwise
           this interface gets Dynamic PPPoE IP from the PPPoE server
    :return: True if successful, otherwise False
    """
    result = True
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intf_url = 'api/fdm/latest/devices/default/interfaces/{}'.format(intf_object['id'])
    intf_object['ipv4']['ipType'] = 'PPPOE'
    intf_object['ipv4']['ipAddress']['ipAddress'] = ip_addr
    if ip_addr == '':
        net_mask = ''
    else:
        net_mask = 32
    intf_object['ipv4']['ipAddress']['netmask'] = net_mask
    intf_object['pppoe'] = pppoe
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intf_url),
        data=json.dumps(intf_object), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT interface response {} {}".format(response.status_code, response.json()))
        result = False
    elif response.status_code == 200:
        print(response.json())
    return result
