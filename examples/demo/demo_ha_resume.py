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
from resources.high_availability import get_ha_status, resume_HA


def main():
    """
    End to end example of code that performs an HA resume and waits for the device to rejoin the HA pair.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values in connection_constants.py in order to connect to your device.
    A deployment will be performed only if the user has made changes on the FTD device and those changes
    are pending at run-time.
    Forgetting to enter the connection_constants or entering the wrong values, and forgetting to make a pending change
    on the FTD device are the most common sources of error.
    """
    host = '10.89.21.72'
    port = '3241'
    user = 'admin'
    passwd = 'Sourcefire'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
    result = resume_HA(host, port, access_token)
    if not result:
        print('Unable to suspend device')
        return
    for _ in range(80):
        (node_state, _, _) = get_ha_status(host=host, port=port, access_token=access_token)
        if not node_state:
            # This is expected if the FTD device was in standby state before being suspended
            print('Unable to obtain ha status')
        elif node_state == 'HA_ACTIVE_NODE' or node_state == 'HA_STANDBY_NODE':
            print("FTD device resumed successfully")
            return
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Unable to restore HA pair')
        return


if __name__ == '__main__':
    main()