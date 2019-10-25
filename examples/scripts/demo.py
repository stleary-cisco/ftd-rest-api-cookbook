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
        response = requests.post("https://{}:{}/api/fdm/latest/fdm/token".format(host, port),
                                 data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("Login successful, access_token obtained {}".format(access_token))
        else:
            print("Login failed {} {}".format(response.status_code, response.json()))
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
    response = requests.get('https://{host}:{port}/{url}'.format(host=host, port=port, url=pending_changes_url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET pending changes response {} {}".format(response.status_code, response.json()))
    else:
        print(response.json())
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
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=deploy_url), verify=False,
                             headers=headers)
    if response.status_code != 200:
        print("Failed POST deploy response {} {}".format(response.status_code, response.json()))
    else:
        print(response.json())
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
    response = requests.get(
        'https://{host}:{port}/{url}/{deploy_id}'.format(host=host, port=port, url=deploy_url, deploy_id=deploy_id),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET deploy response {} {}".format(response.status_code, response.json()))
    else:
        state = response.json().get('state')
        # print(response.json())
        print(state)

    return state


def main():
    """
    End to end example of code that performs an FTD deployment and waits for the deploy task to complete.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values in host, port, user, and passwd in order to connect to your device.
    A deployment will be performed only if the user has made changes on the FTD device and those changes
    are pending at run-time.
    Forgetting to enter the connection_constants or entering the wrong values, and forgetting to make a pending change
    on the FTD device are the most common sources of error.
    """
    host = '10.8.21.72'
    port = '3139'
    user = 'admin'
    passwd = 'Admin123!'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to update connection_constants.py?")
        return
    if get_pending_changes(host, port, access_token):
        deploy_id = post_deployment(host, port, access_token)
        if not deploy_id:
            # should never happen
            print('Unable to obtain a deployment id')
            return
        # wait for a reasonable period of time (about 20 minutes) for the deployment to complete
        for _ in range(80):
            state = get_deployment_status(host, port, access_token, deploy_id)
            if not state:
                # should never happen
                print('Unable to obtain the deployment state')
                return
            elif state == 'DEPLOYED':
                print('Completed deployment successfully')
                return
            elif state == 'DEPLOY_FAILED':
                print('Deployment failed')
                return
            print("sleep 15 seconds")
            time.sleep(15)
        print('Unable to complete the deployment')
    else:
        print("There was nothing to deploy. Did you remember to make a pending change on the FTD device?")


if __name__ == '__main__':
    main()
