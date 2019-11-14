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
from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.ips import get_intrusion_settings, update_intrusion_settings
from ftd_api_resources.syslog_server import post_syslog_server


def ips_syslog_server(host, port, user, passwd):
    """
    End to end example of code that assigns an intrusion rule syslog server.
    Requires Python v3.0 or greater and the reqeusts library.

    :param host: ftd host address
    :param port: ftd host port
    :param user: login username
    :param passwd: login password
    :return: True if successful, otherwise False
    """
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token.")
        return False
    syslog_server = {
        "host": "192.168.100.1",
        "useManagementInterface": True,
        "port": "514",
        "protocol": "UDP",
        "type": "syslogserver"
    }
    syslog_server = post_syslog_server(host, port, access_token, syslog_server)
    if not syslog_server:
        print('Unable to post syslog server')
        return False
    intrusion_settings = get_intrusion_settings(host, port, access_token)
    intrusion_settings["syslogServer"] =  syslog_server
    intrusion_settings = update_intrusion_settings(host, port, access_token, intrusion_settings)
    if not intrusion_settings:
        print('Unable to update intrusion settings')
        return False
    else:
        return True


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 6:
        print("Create a hardcoded syslog server and add it to an intrusion policy.")
        print('Example of a policy_name, enclosed in quotes becuase it includes spaces: "Connectivity over security"')
        print("Usage: python ftd_api_scripts/ips_syslog_server.py host port user passwd policy_name")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    policy_name = sys.argv[5]
    if ips_syslog_server(host, port, user, passwd):
        exit(0)
    else:
        exit(1)