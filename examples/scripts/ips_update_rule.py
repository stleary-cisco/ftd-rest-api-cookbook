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

from cookbook_resources.access_token import get_access_token
from cookbook_resources.ips import get_intrusion_policy, get_intrusion_rule, update_intrusion_rule


def main():
    """
    End to end example of code that updates an intrusion rule.
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
    intrusion_policy = get_intrusion_policy(host, port, access_token, 'Security%20Over%20Connectivity')
    if not intrusion_policy:
        print('Unable to get intrusion policy')
        return
    gid = '1'
    sid = '37244'
    intrusion_rule = get_intrusion_rule(host, port, access_token, intrusion_policy['id'], gid, sid)
    if not intrusion_rule:
        print('Unable to get intrusion rule')
        return
    rule_update = {
        'version': intrusion_policy['version'],
        'id': intrusion_policy['id'],
        'ruleConfigs': [{
            'id': intrusion_rule['id'],
            'state': 'DROP'
        }],
        'type': 'intrusionpolicyruleupdate'
    }
    result = update_intrusion_rule(host, port, access_token, intrusion_policy['id'], rule_update)
    if not result:
        print('Unable to update intrusion rule')
        return
    intrusion_rule = get_intrusion_rule(host, port, access_token, intrusion_policy['id'], gid, sid)
    if not intrusion_rule:
        print('Unable to get intrusion rule')
        return
    print('rule action is {}'.format(intrusion_rule['overrideState']))

if __name__ == '__main__':
    main()
