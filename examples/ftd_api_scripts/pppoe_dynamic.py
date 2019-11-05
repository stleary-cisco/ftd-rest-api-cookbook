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


def pppoe_dynamic(host, port, user, passwd, intf_hw_name='GigabitEthernet1/1', vpdn_grp_name='my_pppoe_group',
                  pppoe_user='my_pppoe_username', pppoe_password='my_pppoe_password', ppp_auth_type='PAP',
                  pppoe_metric=1, obtain_default_route=True):
    """
    End to end example of code that updates a physical interface to enable PPPoE on it.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """
    pppoe = {
        'vpdnGrpName': vpdn_grp_name,
        'pppoeUser': pppoe_user,
        'pppoePassword': pppoe_password,
        'pppAuthType': ppp_auth_type,  # available authentication protocols: PAP, CHAP, MSCHAP
        'pppoeMetric': pppoe_metric,  # integer value with a valid range: 1-255
        'setRoute': obtain_default_route,  # if True, default route will be obtained from the PPPoE server
        'ipIsDynamic': True,
        # if True, then the ipAddress and Netmask should be set to '' in the ipv4 object of an interface object
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
    import sys

    if len(sys.argv) < 5:
        print(
            "Usage: python ftd_api_scripts/pppoe_dynamic.py host port user passwd [intf_hw_name, vpdn_grp_name, pppoe_user, pppoe_password, ppp_auth_type, pppoe_metric, obtain_default_route]")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    # intf_hw_name = sys.argv[5]
    # vpdn_grp_name = sys.argv[6]
    # pppoe_user = sys.argv[7]
    # pppoe_password = sys.argv[8]
    # ppp_auth_type = sys.argv[9]
    # pppoe_metric = sys.argv[10]
    # obtain_default_route = sys.argv[11]
    # if pppoe_dynamic(host=host, port=port, user=user, passwd=passwd, intf_hw_name=intf_hw_name, vpdn_grp_name=vpdn_grp_name, pppoe_user=pppoe_user, pppoe_password=pppoe_password, ppp_auth_type=ppp_auth_type, pppoe_metric=pppoe_metric, obtain_default_route=obtain_default_route):
    if pppoe_dynamic(host=host, port=port, user=user, passwd=passwd):
        exit(0)
    else:
        exit(1)
