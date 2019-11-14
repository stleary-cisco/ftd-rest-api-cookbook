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
from ftd_api_resources.troubleshoot import schedule_troubleshoot, get_troubleshoot_job, download_troubleshoot


def troubleshoot(host, port, user, passwd):
    """
    End to end example of code that creates and downloads a troubleshoot file.
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

    job_id = schedule_troubleshoot(host=host, port=port, access_token=access_token)
    if not job_id:
        # should never happen
        print('Unable to obtain a job id')
        return False
    # wait for a reasonable period of time (about 20 minutes) for the job to complete
    status = None
    filename = None
    for _ in range(80):
        (status, filename) = get_troubleshoot_job(host=host, port=port, access_token=access_token, job_id=job_id)
        if not status:
            # should never happen
            print('Unable to obtain the troubleshoot job status')
            return False
        elif status == 'SUCCESS':
            print('Completed troubleshoot job successfully {}'.format(filename))
            break
        elif status == 'FAILED':
            # should never happen
            print('Troubleshoot job failed')
            return False
        print("sleep 15 seconds")
        time.sleep(15)
    else:
        print('Unable to complete the troubleshoot')
        return False
    try:
        download_troubleshoot(host=host, port=port, access_token=access_token, filename=filename)
        return True
    except Exception as e:
        print('Error when downloading troubleshoot file {}'.format(str(e)))
        return False


if __name__ == '__main__':
    import sys

    if len(sys.argv) != 5:
        print("Create and download a troubleshoot file.")
        print("Usage: python ftd_api_scripts/troubleshoot.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    if troubleshoot(host, port, user, passwd):
        exit(0)
    else:
        exit(1)