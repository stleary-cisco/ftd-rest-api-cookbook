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
import requests

def get_pending_changes(host, port, headers):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a GET rquest to obtain the pending changes from the FTD device
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :return: True if changes are pending, otherwise False
    """
    pending_changes_url = 'api/fdm/latest/operational/pendingchanges'
    response = requests.get('https://{host}:{port}/{url}'.format(host=host, port=port, url=pending_changes_url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET pending changes response {}".format(response.status_code))
    changes_found = True if response.json().get('items') else False
    print("GET pending changes found: {}".format(str(changes_found)))
    return changes_found


def post_deployment(host, port, headers):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a deployment POST request
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :return: unique id for the deployment task
    """
    deploy_url = 'api/fdm/latest/operational/deploy'
    deploy_id = None
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=deploy_url), verify=False,
                             headers=headers)
    if response.status_code != 200:
        print("Failed POST deploy response {}".format(response.status_code))
    else:
        print("POST deployment successful")
        deploy_id = response.json().get('id')
    return deploy_id


def get_deployment_status(host, port, headers, deploy_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Wait for a deployment to complete
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :param deploy_id: unique identifier for deployment task
    """
    deploy_url = 'api/fdm/latest/operational/deploy'
    state = None
    response = requests.get(
        'https://{host}:{port}/{url}/{deploy_id}'.format(host=host, port=port, url=deploy_url, deploy_id=deploy_id),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET deploy response {}".format(response.status_code))
    else:
        state = response.json().get('state')
        print("GET Deployment state: {}".format(state))
    return state
