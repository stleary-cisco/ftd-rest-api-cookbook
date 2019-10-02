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


def get_access_token(host: str, port: str, user: str, passwd: str, headers: {}) -> str:
    """
    Login to FTD device and obtain an access token. The access token is required so that the user can
    connect to the device to send REST API requests.
    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :param headers: HTTP request headers
    :return: OAUTH access token
    """
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {**headers, 'Authorization': 'Bearer '}
    try:
        response = requests.post("https://{}:{}/api/fdm/latest/fdm/token".format(host, port),
                             data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("Login successful, access_token obtained")
    except Exception as e:
        print("Unable to POST access token request: {}".format(str(e)))

    return access_token
