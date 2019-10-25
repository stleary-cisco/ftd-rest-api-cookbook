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


def get_intrusion_policy(host, port, access_token, policy_name):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an intrusion policy GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param policy_name: URL encoded name of the policy to retrieve
    :return: intrusion policy object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intrusion_policy = None
    intrusion_policy_url = 'api/fdm/latest/policy/intrusionpolicies?filter=name:{}'.format(policy_name)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intrusion_policy_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET intrusion policy response {} {}".format(response.status_code, response.json()))
    else:
        intrusion_policy = response.json().get('items')[0]
        print('Intrusion policy found: {}'.format(str(intrusion_policy)))
    return intrusion_policy


def get_intrusion_rule(host, port, access_token, policy_id, gid, sid):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an intrusion rule GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param policy_id: unique identifier for intrusion policy that owns the rule
    :param gid: intrusion rule group identifier
    :param sid: intrusion rule signature identifier
    :return: intrusion rule object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intrusion_rule = None
    intrusion_rule_url = 'api/fdm/latest/policy/intrusionpolicies/{}/intrusionrules?filter=gid:{};sid:{}'.format(
        policy_id, gid, sid)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intrusion_rule_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET intrusion rule response {} {}".format(response.status_code, response.json()))
    else:
        intrusion_rule = response.json().get('items')[0]
        print('Intrusion rule found: {}'.format(str(intrusion_rule)))
    return intrusion_rule


def update_intrusion_rule(host, port, access_token, policy_id, rule_update):
    """
    Requires Python v3.0 or greater and requests lib.
    Update an intrusion rule
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param policy_id: unique identifier for intrusion policy that owns the rule
    :param rule_update: intrusion rule update object
    :return: True if successful, otherwise False
    """
    result = True
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intrusion_rule_url = 'api/fdm/latest/policy/intrusionpolicies/{}/ruleupdates'.format(policy_id)
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intrusion_rule_url),
        data=json.dumps(rule_update), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT intrusion rule response {} {}".format(response.status_code, response.json()))
        result = False
    elif response.status_code == 200:
        print(response.json())
    return result


def post_access_rule(host, port, access_token, access_rule):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an access rules POST request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param access_rule: object representing the access rule
    :return: True if successful, otherwise False
    """
    result = True
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    access_rule_url = 'api/fdm/latest/policy/accesspolicies/default/accessrules?at=0'
    response = requests.post(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=access_rule_url),
        data=json.dumps(access_rule), verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST access rule response {} {}".format(response.status_code, response.json()))
        result = False
    else:
        print(response.json())
    return result


def get_intrusion_settings(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an intrusion settings GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: intrusion settings object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intrusion_settings = None
    intrusion_settings_url = 'api/fdm/latest/object/intrusionsettings'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intrusion_settings_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET intrusion settings response {} {}".format(response.status_code, response.json()))
    else:
        intrusion_settings = response.json().get('items')[0]
        print('Intrusion settings found: {}'.format(str(intrusion_settings)))
    return intrusion_settings


def update_intrusion_settings(host, port, access_token, intrusion_settings):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an intrusion settings PUT request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param intrusion_settings: intrusion settings object
    :return: True if successful, otherwise false
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    intrusion_settings_url = 'api/fdm/latest/object/intrusionsettings/{}'.format(intrusion_settings['id'])
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=intrusion_settings_url),
        data=json.dumps(intrusion_settings), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT intrusion settings response {} {}".format(response.status_code, response.json()))
        intrusion_settings = None
        result = False
    elif response.status_code == 200:
        intrusion_settings = response.json()
        print(response.json())
    return intrusion_settings
