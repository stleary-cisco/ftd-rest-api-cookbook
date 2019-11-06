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


def get_all_timezone_setting(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send timezone setting GETALL request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: timezone-setting
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    timezone_setting = None
    timezone_setting_url = 'api/fdm/latest/devicesettings/default/timezonesettings'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=timezone_setting_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET timezone-setting response {} {}".format(response.status_code, response.json()))
    else:
        timezone_setting = response.json().get('items')[0]
        print('timezone-setting found: {}'.format(str(timezone_setting)))
    return timezone_setting


def update_timezone_setting(host, port, access_token, timezone_setting_id, timezone_setting_update):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an timezone setting PUT request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param timezone_setting_id: unique identifier for a timezone-setting
    :param timezone_setting_update: updated timezone-setting
    :return: updated timezone setting
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    timezone_setting_url = 'api/fdm/latest/devicesettings/default/timezonesettings/{}'.format(timezone_setting_id)
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=timezone_setting_url),
        data=json.dumps(timezone_setting_update), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT timezone-setting response {} {}".format(response.status_code, response.json()))
        timezone_setting_update = None
    elif response.status_code == 200:
        print(response.json())
        timezone_setting_update = response.json()
    return timezone_setting_update


def get_timezone_setting(host, port, access_token, timezone_setting_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send an timezone setting GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param timezone_setting_id: unique identifier for a timezone setting
    :return: timezone setting
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    timezone_setting = None
    timezone_setting_url = 'api/fdm/latest/devicesettings/default/timezonesettings/{}'.format(timezone_setting_id)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=timezone_setting_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET timezone-setting response {} {}".format(response.status_code, response.json()))
    else:
        timezone_setting = response.json()
        print('timezone-setting found: {}'.format(str(timezone_setting)))
    return timezone_setting