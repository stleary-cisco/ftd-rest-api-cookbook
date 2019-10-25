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
from cookbook_resources.access_token import get_access_token
from cookbook_resources.ips import get_intrusion_settings, update_intrusion_settings
from cookbook_resources.syslog_server import post_syslog_server


def main():
    """
    End to end example of code that assigns an intrusion rule syslog server.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """
    host = 'ftd.example'
    port = '443'
    user = 'admin'
    passwd = 'Admin123'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
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
        return
    intrusion_settings = get_intrusion_settings(host, port, access_token)
    intrusion_settings["syslogServer"] =  syslog_server
    intrusion_settings = update_intrusion_settings(host, port, access_token, intrusion_settings)
    if not intrusion_settings:
        print('Unable to update intrusion settings')
        return


if __name__ == '__main__':
    main()
