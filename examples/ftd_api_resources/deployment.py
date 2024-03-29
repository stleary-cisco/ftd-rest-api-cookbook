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


def get_access_token(host, port, user, passwd):
    """
    Requires Python v3.0 or greater and requests lib.
    Login to FTD device and obtain an access token. The access token is required so that the user can
    connect to the device to send REST API requests.
    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :return: OAUTH access token
    """
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {"Content-Type": "application/json", "Accept": "application/json"}
    try:
        url = "https://{}:{}/api/fdm/latest/fdm/token".format(host, port)
        print('GET access token URL: {}'.format(url))
        print('GET access token Payload: {}'.format(payload))
        response = requests.post(url, data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            print('{} {}'.format(response.status_code, response.json()))
            access_token = response.json().get('access_token')
            print("Login successful")
        else:
            print("{} {}".format(response.status_code, response.json()))
    except Exception as e:
        print("Exception in POST access token request: {}".format(str(e)))
    return access_token


def get_pending_changes(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a GET rquest to obtain the pending changes from the FTD device
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :return: True if changes are pending, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    changes_found = False
    pending_changes_url = 'api/fdm/latest/operational/pendingchanges'
    url = 'https://{host}:{port}/{url}'.format(host=host, port=port, url=pending_changes_url)
    print('GET pending changes URL: {}'.format(url))
    response = requests.get(url, verify=False, headers=headers)
    print("{} {}".format(response.status_code, response.json()))
    if response.status_code == 200:
        if response.json().get('items'):
            changes_found = True
    return changes_found


def post_deployment(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a deployment POST request
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :return: unique id for the deployment task
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    deploy_id = None
    deploy_url = 'api/fdm/latest/operational/deploy'
    url = 'https://{host}:{port}/{url}'.format(host=host, port=port, url=deploy_url)
    print('POST deployment URL: {}'.format(url))
    response = requests.post(url, verify=False,
                             headers=headers)
    print("{} {}".format(response.status_code, response.json()))
    if response.status_code == 200:
        deploy_id = response.json().get('id')
    return deploy_id


def get_deployment_status(host, port, access_token, deploy_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Wait for a deployment to complete
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :param deploy_id: unique identifier for deployment task
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    state = None
    deploy_url = 'api/fdm/latest/operational/deploy'
    url = 'https://{host}:{port}/{url}/{deploy_id}'.format(host=host, port=port, url=deploy_url, deploy_id=deploy_id)
    print('GET deployment URL: {}'.format(url))
    response = requests.get(
        url,
        verify=False, headers=headers)
    print("{}".format(response.status_code))
    if response.status_code == 200:
        state = response.json().get('state')
        print(state)
    return state
