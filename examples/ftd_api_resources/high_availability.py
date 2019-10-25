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

import requests


def get_ha_status(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an HA status GET request to a device in an HA pair.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: HA node state, peer node state, and config status
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    node_state = None
    peer_node_state = None
    config_status = None
    ha_status_url = 'api/fdm/latest/devices/default/operational/ha/status/default'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=ha_status_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET HA status response {} {}".format(response.status_code, response.json()))
    else:
        node_state = response.json().get('nodeState')
        peer_node_state = response.json().get('peerNodeState')
        config_status = response.json().get('configStatus')
        print("GET HA status nodeState {}  peerNodeState {} configStatus {}".format(node_state, peer_node_state,
                                                                                    config_status))
    return (node_state, peer_node_state, config_status)


def suspend_HA(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an HA suspend POST request a device in an HA pair.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: True if successful, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    suspend_ha_url = 'api/fdm/latest/devices/default/action/ha/suspend'
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=suspend_ha_url),
                             verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST suspend HA response {} {}".format(response.status_code, response.json()))
        return False
    else:
        print('HA suspended successfully')
        return True


def resume_HA(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an HA resume POST request to a device in an HA pair.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: True if successful, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    resume_ha_url = 'api/fdm/latest/devices/default/action/ha/resume'
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=resume_ha_url),
                             verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST resume HA response {} {}".format(response.status_code, response.json()))
        return False
    else:
        print('HA resumed successfully')
        return True


def post_break_ha(host, port, access_token, clearIntfs=False):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an HA break POST request to a device in an HA pair.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param clearIntfs: True if interfaces should be cleared, otherwise False
    :param break_id: unique id of the ha break task
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    break_ha_id = None
    break_ha_url = 'api/fdm/latest/devices/default/action/ha/break?clearIntfs='
    if clearIntfs:
        break_ha_url += 'true'
    else:
        break_ha_url += 'false'
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=break_ha_url),
                             verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST break HA response {} {}".format(response.status_code, response.json()))
    else:
        break_ha_id = response.json().get('id')
        print("Break HA posted successfully {}".format(break_ha_id))
    return break_ha_id


def get_break_ha(host, port, access_token, break_ha_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an HA break status request to a device in an HA pair.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param break_ha_id: unique identifier for break ha task
    :return: break ha state
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    state = None
    break_ha_url = 'api/fdm/latest/devices/default/action/ha/break/{}'.format(break_ha_id)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=break_ha_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET break HA state {} {}".format(response.status_code, response.json()))
    else:
        state = response.json().get('state')
        print("GET break HA state {}".format(state))
    return state
