import time
from demo.connection_constants import host, port, user, passwd, headers
from resources.deployment import get_pending_changes, post_deployment, get_deployment_status
from resources.access_token import get_access_token

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

def main():
    access_token = get_access_token(host, port, user, passwd, headers)
    if not access_token:
        return
    request_headers = {**headers, "Authorization" : "Bearer {}".format(access_token)}
    if get_pending_changes(host=host, port=port, headers=request_headers):
        id = post_deployment(host=host, port=port, headers=request_headers)
        if not id:
            return
        for _ in range(80):
            state = get_deployment_status(host=host, port=port, headers=request_headers, id=id)
            if not state or state == 'DEPLOYED' or state == 'FAILED':
                return
            print("sleep 15 seconds")
            time.sleep(15)
        print('Unable to complete the deployment')


if __name__ == '__main__':
    main()