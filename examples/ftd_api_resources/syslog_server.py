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


def post_syslog_server(host, port, access_token, syslog_server):
    """
    Requires Python v3.0 or greater and requests lib.
    Send syslog server POST request.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param syslog_server: object representing the syslog server
    :return: True if successful, otherwise False
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    syslog_server_url = 'api/fdm/latest/object/syslogalerts'
    response = requests.post(
        'https://{host}:{port}/{url}'.format(host=host, port=port, url=syslog_server_url),
        data=json.dumps(syslog_server), verify=False, headers=headers)
    if response.status_code != 200 and response.status_code != 204:
        print("Failed POST syslog server response {} {}".format(response.status_code, response.json()))
        syslog_server = None
    elif response.status_code == 200:
        syslog_server = response.json()
        print(response.json())
    return syslog_server
