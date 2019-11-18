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

from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.smart_agent import post_smart_agent_sync_requests


def sync(host, port, user, passwd):
    """
    Example of code that disables license by type name.
    Preconditions: device is registered in Smart License.
    Requires Python v3.0 or greater and the requests library.
    """
    access_token = get_access_token(host, port, user, passwd)

    if not access_token:
        raise Exception('Unable to obtain an access token.')

    post_smart_agent_sync_requests(host, port, access_token)


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Usage: python ftd_api_scripts/smart_license_sync.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]

    try:
        sync(host, port, user, passwd)
        exit(0)
    except Exception as e:
        print("Error: {}".format(e))
        exit(1)