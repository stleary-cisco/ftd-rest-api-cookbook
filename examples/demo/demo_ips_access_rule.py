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
from resources.ips import get_intrusion_policy, post_access_rule
from resources.smart_license import get_smart_licenses, post_smart_license


def main():
    """
    End to end example of code that creates an access rule with an intrusion policy.
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
    smart_licenses = get_smart_licenses(host, port, access_token)
    for smart_license in smart_licenses:
        if smart_license['licenseType'] == 'THREAT':
            print('threat license found')
            break
    else:
        threat_license = {
            'type': 'license',
            'count': 1,
            'licenseType': 'THREAT'
        }
        result = post_smart_license(host, port, access_token, threat_license)
        if not result:
            print('Unable to post threat license')
    if not smart_licenses:
        print('Unable to get smart licenses')
        return
    intrusion_policy = get_intrusion_policy(host, port, access_token, 'Security%20Over%20Connectivity')
    if not intrusion_policy:
        print('Unable to get intrusion policy')
        return
    access_rule = {
        "type": "accessrule",
        "name": "myName",
        "ruleAction": "PERMIT",
        "eventLogAction": "LOG_BOTH",
        "intrusionPolicy": {
            "type": "intrusionpolicy",
            "id": intrusion_policy['id']
        }
    }
    result = post_access_rule(host, port, access_token, access_rule)
    if not result:
        print('Unable to post access rule')
        return

if __name__ == '__main__':
    main()
