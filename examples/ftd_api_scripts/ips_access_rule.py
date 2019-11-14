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
from ftd_api_resources.ips import get_intrusion_policy, post_access_rule
from ftd_api_resources.smart_license import get_smart_licenses, post_smart_license


def ips_access_rule(host, port, user, passwd, policy_name):
    """
    End to end example of code that creates an access rule with an intrusion policy.
    The access rule is added to the start of the access rule list.
    Requires Python v3.0 or greater and the reqeusts library.

    :param host: ftd host address
    :param port: ftd host port
    :param user: login username
    :param passwd: login password
    :param policy_name: intrusion policy to include in access rule
    :return: True if successful, otherwise False
    """
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token.")
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
        return False
    intrusion_policy = get_intrusion_policy(host, port, access_token, policy_name)
    if not intrusion_policy:
        print('Unable to get intrusion policy')
        return False
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
        return False
    else:
        return True

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 6:
        print("Usage: python ftd_api_scripts/ips_access_rule.py host port user passwd policy_name")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    policy_name = sys.argv[5]
    if ips_access_rule(host, port, user, passwd, policy_name):
        exit(0)
    else:
        exit(1)