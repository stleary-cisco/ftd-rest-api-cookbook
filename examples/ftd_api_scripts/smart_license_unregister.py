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
from ftd_api_resources.smart_agent import get_smart_agent_connections, get_smart_agent_statuses, \
    delete_smart_agent_connection
from ftd_api_resources.smart_license_job import get_last_smart_license_unregistration_job_status


def unregister(host, port, user, passwd):
    """
    Example of code that performs unregistration in Smart License and waits for unregistration job completion.
    Requires Python v3.0 or greater and the requests library.
    """
    access_token = get_access_token(host, port, user, passwd)

    if not access_token:
        raise Exception("Unable to obtain an access token.")

    smart_agent_connections = get_smart_agent_connections(host, port, access_token)
    if not smart_agent_connections:
        raise Exception("Device is already unregistered.")

    delete_smart_agent_connection(host, port, access_token, smart_agent_connections[0]["id"])

    status = ""
    # wait for a reasonable period of time (about 20 minutes) for job to complete
    for _ in range(0, 60):
        print("Waiting 10 seconds to complete Smart License Un-registration job...")
        time.sleep(10)
        status = get_last_smart_license_unregistration_job_status(host, port, access_token)
        if status != "IN_PROGRESS":
            break

    if status == "SUCCESS":
        print("Smart License successfully unregistered.")
    else:
        raise Exception("Smart License Un-registration job has status: {}. Expected: SUCCESS".format(status))

    if len(get_smart_agent_connections(host, port, access_token)) != 0:
        raise Exception("Smart Agent Connection was not removed.")

    if get_smart_agent_statuses(host, port, access_token)[0]['registrationStatus'] != 'UNREGISTERED':
        raise Exception("Smart Agent Status is invalid. Expected = 'UNREGISTERED'.")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 5:
        print("Usage: python ftd_api_scripts/smart_license_unregister.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]

    try:
        unregister(host, port, user, passwd)
        exit(0)
    except Exception as e:
        print("Error: {}".format(e))
        exit(1)
