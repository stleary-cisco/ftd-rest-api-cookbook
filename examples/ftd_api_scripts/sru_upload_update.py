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

import argparse
import time
from ftd_api_resources.access_token import get_access_token
from ftd_api_resources.sru_manual_update import send_sru_update_file, fetch_all_sru_jobs, fetch_sru_job_by_id


def main():
    # read the commandline arguments
    parser = argparse.ArgumentParser(description='Upload an SRU update file then track the update job.')

    parser.add_argument('-u', '--user-name', help='name of your API user', required=True, default='1')
    parser.add_argument('-p', '--password', help='password of your API user', required=True, default='1')
    parser.add_argument('-a', '--host', help='FTD host without port', required=True, default='1')
    parser.add_argument('-n', '--port', help='FTD port number', required=True, default='1')
    parser.add_argument('-f', '--file', help='path to update file', required=True, default='1')

    args = parser.parse_args()

    user_name = args.user_name
    password = args.password
    host = args.host
    port = args.port
    file = args.file

    # send the update file
    auth_token = get_access_token(host, port, user_name, password)
    update_code = send_sru_update_file(host, port, auth_token, file)
    if update_code != 200:
        print("Upload failed. Aborting.")
        exit(1)
    print("Upload Successful.")

    # get the uuid of the update job
    jobs = fetch_all_sru_jobs(host, port, auth_token)
    if jobs is None:
        print('Failed to get update jobs. Aborting.')
        exit(0)

    current_job = jobs[0]
    current_job_uuid = current_job.get('id')

    # send periodic status checks for up to 5 minutes
    try_count = 0
    while try_count < 30:
        current_job = fetch_sru_job_by_id(host, port, auth_token, current_job_uuid)
        status = current_job.get('status')

        # check the job status
        if status == 'SUCCESS':
            print('Update job was successful!')
            exit(0)

        if status == 'FAILED':
            print('Update job was not successful.')
            exit(0)

        # job is still in progress; wait for 10 seconds and try again
        print('Update job is still in progress. Check again in 10 seconds.')
        time.sleep(10)
        try_count += 1

    print('Update job is still in progress after 5 minutes.')
    exit(0)


if __name__ == "__main__":
    main()
