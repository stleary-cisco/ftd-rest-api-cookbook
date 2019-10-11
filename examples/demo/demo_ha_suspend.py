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
from resources.access_token import get_access_token
from resources.high_availability import get_ha_status, suspend_HA


def main():
    """
    End to end example of code that suspends a device in a HA pair.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """
    host = 'ftd.example'
    port = '443'
    user = 'admin'
    passwd = 'Admin123'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
    result = suspend_HA(host, port, access_token)
    if not result:
        print('Unable to suspend device')
        return
    for _ in range(80):
        (node_state, _, _) = get_ha_status(host=host, port=port, access_token=access_token)
        if not node_state:
            # should never happen
            print('Unable to obtain ha status')
            return
        if node_state == 'HA_SUSPENDED_NODE':
            print("FTD device suspended successfully")
            return
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Never reached suspended state')
        return


if __name__ == '__main__':
    main()
