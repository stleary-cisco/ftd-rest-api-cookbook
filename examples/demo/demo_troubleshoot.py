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
from resources.access_token import get_access_token
from resources.troubleshoot import schedule_troubleshoot, get_troubleshoot_job, download_troubleshoot


def main():
    """
    End to end example of code that performs an FTD deployment and waits for the deploy task to complete.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    A deployment will be performed only if the user has made changes on the FTD device and those changes
    are pending at run-time.
    Forgetting to enter the connection_constants or entering the wrong values, and forgetting to make a pending change
    on the FTD device are the most common sources of error.
    """
    host = 'ftd.example'
    port = '443'
    user = 'admin'
    passwd = 'Admin123'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return

    job_id = schedule_troubleshoot(host=host, port=port, access_token=access_token)
    if not job_id:
        # should never happen
        print('Unable to obtain a job id')
        return
    # wait for a reasonable period of time (about 20 minutes) for the job to complete
    status = None
    filename = None
    for _ in range(80):
        (status, filename) = get_troubleshoot_job(host=host, port=port, access_token=access_token, job_id=job_id)
        if not status:
            # should never happen
            print('Unable to obtain the troubleshoot job status')
            return
        elif status == 'SUCCESS':
            print('Completed troubleshoot job successfully {}'.format(filename))
            break
        elif status == 'FAILED':
            # should never happen
            print('Troubleshoot job failed')
            return
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Unable to complete the troubleshoot')
        return
    download_troubleshoot(host=host, port=port, access_token=access_token, filename=filename)


if __name__ == '__main__':
    main()
