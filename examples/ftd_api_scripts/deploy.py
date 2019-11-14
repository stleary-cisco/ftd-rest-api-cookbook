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
from ftd_api_resources.deployment import get_pending_changes, post_deployment, get_deployment_status
from ftd_api_resources.access_token import get_access_token

def deploy(host, port, user, passwd):
    '''

    '''
    """
    End to end example of code that performs an FTD deployment and waits for the deploy task to complete.
    A deployment will be performed only if the user has made changes on the FTD device and those changes
    are pending at run-time.
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
    if get_pending_changes(host, port, access_token):
        deploy_id = post_deployment(host, port, access_token)
        if not deploy_id:
            # should never happen
            print('Unable to obtain a deployment id')
            return False
        # wait for a reasonable period of time (about 20 minutes) for the deployment to complete
        for _ in range(80):
            state = get_deployment_status(host, port, access_token, deploy_id)
            if not state:
                # should never happen
                print('Unable to obtain the deployment state')
                return False
            elif state == 'DEPLOYED':
                print('Completed deployment successfully')
                return True
            elif state == 'DEPLOY_FAILED':
                print('Deployment failed')
                return False
            print("sleep 15 seconds")
            time.sleep(15)
        print('Unable to complete the deployment')
        return False
    else:
        print("There was nothing to deploy.")
        return True

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Perform a deployment operation.")
        print("Usage: python ftd_api_scripts/deploy.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    if deploy(host, port, user, passwd):
        exit(0)
    else:
        exit(1)
