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

import time
from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.high_availability import get_ha_status, reset_HA


def ha_reset(host, port, user, passwd):
    """
    End to end example of code that performs an HA reset.
    Requires Python v3.0 or greater and the reqeusts library.

    :param host: ftd host address
    :param port: ftd host port
    :param user: login username
    :param passwd: login password
    :return: True if successful, otherwise False
    """
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token.")
        return
    result = reset_HA(host, port, access_token)
    if not result:
        print('Unable to reset device')
        return
    for _ in range(80):
        (node_state, _, _) = get_ha_status(host=host, port=port, access_token=access_token)
        if not node_state:
            print('Unable to obtain ha status')
        elif node_state == 'HA_ACTIVE_NODE' or node_state == 'HA_STANDBY_NODE':
            print("FTD device reset successfully")
            return
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Unable to reset HA device')
        return


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Send a reset request to a device in an HA pair")
        print("Usage: python ftd_api_scripts/ha_reset.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    if ha_reset(host, port, user, passwd):
        exit(0)
    else:
        exit(1)
