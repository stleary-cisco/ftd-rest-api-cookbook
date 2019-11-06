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


def get_all_time_zones(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send time zone objects GETALL request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: time-zone objects
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    timezone_objects = None
    tzo_url = 'api/fdm/latest/object/timezoneobjects'
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=tzo_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET time zone objects response {} {}".format(response.status_code, response.json()))
    else:
        timezone_objects = response.json().get('items')
        print('time range objects found: {}'.format(str(timezone_objects)))
    return timezone_objects


def post_time_zone(host, port, access_token, tzo_object):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a time zone object POST request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param tzo_object: object representing the time-zone
    :return: time-zone object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    tzo_url = 'api/fdm/latest/object/timezoneobjects'
    response = requests.post(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=tzo_url),
        data=json.dumps(tzo_object), verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST time zone object response {} {}".format(response.status_code, response.json()))
        tro_object = None
    else:
        print(response.json())
        tro_object = response.json()
    return tro_object


def update_time_zone(host, port, access_token, tzo_id, tzo_object_update):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a time zone object PUT request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param tzo_id: unique identifier for a time-zone object
    :param tzo_object_update: updated time-zone object
    :return: time-zone object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    tzo_url = 'api/fdm/latest/object/timezoneobjects/{}'.format(tzo_id)
    response = requests.put(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=tzo_url),
        data=json.dumps(tzo_object_update), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed PUT time-zone object response {} {}".format(response.status_code, response.json()))
        tzo_object_update = None
    elif response.status_code == 200:
        print(response.json())
        tzo_object_update = response.json()
    return tzo_object_update


def get_time_zone(host, port, access_token, tzo_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a time zone object GET request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param tzo_id: unique identifier for a time-zone object
    :return: time-zone object
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    timezone_object = None
    tzo_url = 'api/fdm/latest/object/timezoneobjects/{}'.format(tzo_id)
    response = requests.get(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=tzo_url),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET time zone objects response {} {}".format(response.status_code, response.json()))
    else:
        timezone_object = response.json()
        print('time zone object found: {}'.format(str(timezone_object)))
    return timezone_object


def delete_time_zone(host, port, access_token, tzo_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a time zone object DELETE request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param tzo_id: unique identifier for time-zone object
    :return: response status code
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    status_code_for_delete_operation = None
    tzo_url = 'api/fdm/latest/object/timezoneobjects/{}'.format(tzo_id)
    response = requests.delete(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=tzo_url),
        verify=False, headers=headers)
    if response.status_code != 204:
        print("Failed DELETE time zone object response {} {}".format(response.status_code, response.json()))
    else:
        status_code_for_delete_operation = response.status_code
        print('time zone object is deleted, error code is: {}'.format(status_code_for_delete_operation))
    return status_code_for_delete_operation
