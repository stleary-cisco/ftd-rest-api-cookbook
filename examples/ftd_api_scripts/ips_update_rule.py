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
from ftd_api_resources.ips import get_intrusion_policy, get_intrusion_rule, update_intrusion_rule


def ips_update_rule(host, port, user, passwd, policy_name, gid, sid, state):
    """
    End to end example of code that updates an intrusion rule for an intrusion policy.
    Requires Python v3.0 or greater and the reqeusts library.

    :param host: ftd host address
    :param port: ftd host port
    :param user: login username
    :param passwd: login password
    :param policy_name: name of the policy to update
    :param gid: group id of the rule to update
    :param sid: signature id of the rule to update
    :param state: override state of the rule to update
    :return: True if successful, otherwise False
    """
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token.")
        return False
    intrusion_policy = get_intrusion_policy(host, port, access_token, policy_name)
    if not intrusion_policy:
        print('Unable to get intrusion policy')
        return False
    intrusion_rule = get_intrusion_rule(host, port, access_token, intrusion_policy['id'], gid, sid)
    if not intrusion_rule:
        print('Unable to get intrusion rule')
        return False
    rule_update = {
        'version': intrusion_policy['version'],
        'id': intrusion_policy['id'],
        'ruleConfigs': [{
            'id': intrusion_rule['id'],
            'state': state
        }],
        'type': 'intrusionpolicyruleupdate'
    }
    result = update_intrusion_rule(host, port, access_token, intrusion_policy['id'], rule_update)
    if not result:
        print('Unable to update intrusion rule')
        return False
    intrusion_rule = get_intrusion_rule(host, port, access_token, intrusion_policy['id'], gid, sid)
    if not intrusion_rule:
        print('Unable to get intrusion rule')
        return False
    print('rule action is {}'.format(intrusion_rule['overrideState']))
    return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 9:
        print("Update an intrusion rule action in an intrusion policy.")
        print('Example of a policy_name, enclosed in quotes becuase it includes spaces: "Connectivity over security"')
        print("Usage: python ftd_api_scripts/ips_update_rule.py host port user passwd policy_name gid sid state")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    policy_name = sys.argv[5]
    gid = sys.argv[6]
    sid = sys.argv[7]
    state = sys.argv[8]
    if ips_update_rule(host, port, user, passwd, policy_name, gid, sid, state):
        exit(0)
    else:
        exit(1)
