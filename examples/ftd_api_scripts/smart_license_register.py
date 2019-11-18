"""
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

"""

import time

from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.smart_agent import post_smart_agent_connection, get_smart_agent_connections, \
    get_smart_agent_statuses
from ftd_api_resources.smart_license_job import get_last_smart_license_registration_job_status


def register(host, port, user, passwd, token):
    """
    Example of code that performs registration in Smart License and waits for registration job completion.
    Requires Python v3.0 or greater and the requests library.

    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :param token: smart license token
    """
    access_token = get_access_token(host, port, user, passwd)

    if not access_token:
        raise Exception("Unable to obtain an access token.")

    post_smart_agent_connection(host, port, access_token, token)

    status = ""
    for i in range(0, 15):
        print("Waiting 5 seconds to complete Smart License Registration job...")
        time.sleep(5)
        status = get_last_smart_license_registration_job_status(host, port, access_token)
        if status != "IN_PROGRESS":
            break

    if status == "SUCCESS":
        print("Smart License successfully registered.")
    else:
        raise Exception("Smart License Registration job has status: {}. Expected: SUCCESS".format(status))

    assert len(get_smart_agent_connections(host, port, access_token)) == 1
    assert get_smart_agent_statuses(host, port, access_token)[0]['registrationStatus'] == 'REGISTERED'


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 6:
        print("Usage: python ftd_api_scripts/smart_license_register.py host port user passwd token")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    token = sys.argv[5]

    try:
        register(host, port, user, passwd, token)
        exit(0)
    except Exception as e:
        print("Error: {}".format(e))
        exit(1)
