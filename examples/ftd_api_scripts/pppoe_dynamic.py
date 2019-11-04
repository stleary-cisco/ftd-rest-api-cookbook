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

from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.interface import get_intf_object
from ftd_api_resources.pppoe import update_intf_to_pppoe


def main():
    """
    End to end example of code that updates a physical interface to enable PPPoE on it.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """
    host = 'fdm-ss-5516.cisco.com'
    port = '443'
    user = 'admin'
    passwd = 'Admin123'

    """
    Example values to enable PPPoE on an interface
    You need to update these values to suit your needs
    """

    intf_hw_name = 'GigabitEthernet1/1'

    pppoe = {
        'vpdnGrpName': 'my_pppoe_group',
        'pppoeUser': 'my_pppoe_username',
        'pppoePassword': 'my_pppoe_password',
        'pppAuthType': 'PAP',
        'pppoeMetric': 1,
        'setRoute': True,
        'ipIsDynamic': True,
        'type': 'pppoverethernet'
    }

    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
    intf_object = get_intf_object(host, port, access_token, intf_hw_name)
    if not intf_object:
        print(
            'Unable to get intf_object - please set the intf_hw_name to a valid hardwareName of an interface on your device')
        return

    # Enable Dynamic PPPoE on interface
    result = update_intf_to_pppoe(host, port, access_token, intf_object, pppoe)
    if not result:
        print('Unable to update intf to enable pppoe')
        return
    else:
        print('Interface {} successfully set to Dynamic PPPoE'.format(intf_hw_name))


if __name__ == '__main__':
    main()
