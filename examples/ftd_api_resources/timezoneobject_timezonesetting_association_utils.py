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

import json
import requests


def get_all_access_rules(host, port, access_token, parent_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send access rules GETALL request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param parent_id: unique identifier for parent access policy
    :return: access rules
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    access_rules = None
    access_rules_url = 'api/fdm/latest/policy/accesspolicies/{}/accessrules'.format(parent_id)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=access_rules_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET access rules response {} {}".format(response.status_code, response.json()))
    else:
        access_rules = response.json().get('items')
        print('access rules found: {}'.format(str(access_rules)))
    return access_rules


def post_access_rule(host, port, access_token, access_rule, parent_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an access rule POST request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param access_rule: object representing the access rule
    :param parent_id: unique identifier for parent access policy
    :return: access rule
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    access_rule_url = 'api/fdm/latest/policy/accesspolicies/{}/accessrules'.format(parent_id)
    response = requests.post(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=access_rule_url),
        data=json.dumps(access_rule), verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST access rule response {} {}".format(response.status_code, response.json()))
        access_rule = None
    else:
        print(response.json())
        access_rule = response.json()
    return access_rule


def update_access_rule(host, port, access_token, access_rule_id, access_rule_update, parent_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an access rule PUT request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param access_rule_id: unique identifier for an access rule
    :param access_rule_update: updated access rule
    :param parent_id: unique identifier for parent access policy
    :return: updated access rule
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    access_rule_url = 'api/fdm/latest/policy/accesspolicies/{}/accessrules/{}'.format(parent_id, access_rule_id)
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=access_rule_url),
        data=json.dumps(access_rule_update), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT access rule response {} {}".format(response.status_code, response.json()))
        access_rule_update = None
    elif response.status_code == 200:
        print(response.json())
        access_rule_update = response.json()
    return access_rule_update


def get_access_rule(host, port, access_token, access_rule_id, parent_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an access rule GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param access_rule_id: unique identifier for an access rule
    :param parent_id: unique identifier for parent access policy
    :return: True if successful, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    access_rule = None
    access_rule_url = 'api/fdm/latest/policy/accesspolicies/{}/accessrules/{}'.format(parent_id, access_rule_id)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=access_rule_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET access rule response {} {}".format(response.status_code, response.json()))
    else:
        access_rule = response.json()
        print('access rule found: {}'.format(str(access_rule)))
    return access_rule