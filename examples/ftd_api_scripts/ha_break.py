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
from ftd_api_resources.high_availability import get_ha_status, post_break_ha, get_break_ha


def ha_break(host, port, user, passwd):
    """
    End to end example of code that performs an HA break break task to complete.
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
        return False

    ha_status = get_ha_status(host=host, port=port, access_token=access_token)
    node_state = ha_status.get('node_state')
    peer_node_state = ha_status.get('peer_node_state')
    config_status = ha_status.get('config_status')
    if not node_state or not peer_node_state or not config_status:
        # should never happen
        print('Unable to obtain ha status')
        return False
    if node_state == 'HA_CONFIGURATION_SYNC' or peer_node_state == 'HA_CONFIGURATION_SYNC' or \
                    config_status == 'PRIMARY_IMPORTING_CONFIG' or config_status == 'SECONDARY_IMPORTING_CONFIG':
        print('Invalid ha status for break: node {} peer {} configStatus {}'.format(node_state, peer_node_state,
                                                                                    config_status))
        return False
    break_ha_id = post_break_ha(host=host, port=port, access_token=access_token, interface_option='DISABLE_INTERFACES')
    if not break_ha_id:
        print('Unable to obtain break id')
        return False
    for _ in range(80):
        state = get_break_ha(host=host, port=port, access_token=access_token, break_ha_id=break_ha_id)
        if state == 'DEPLOYED':
            break
        elif state == 'FAILED':
            print('Unable to complete break deployment')
            return False
        else:
            print("sleep 15 seconds")
            time.sleep(15)
    else:
        print('Unable to complete break')
        return False

    for _ in range(80):
        (node_state, _, _) = get_ha_status(host=host, port=port, access_token=access_token)
        if not node_state:
            # should never happen
            print('Unable to obtain ha status')
            return False
        if node_state == 'SINGLE_NODE':
            print("HA break completed successfully")
            return True
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Unable to complete break')
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Usage: python ftd_api_scripts/ha_break.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    if ha_break(host, port, user, passwd):
        exit(0)
    else:
        exit(1)