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

import requests


def schedule_troubleshoot(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a schedule troubleshoot POST request to an FTD device
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :return: schedule troubleshoot id
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    schedule_troubleshoot_id = None
    schedule_troubleshoot_url = 'api/fdm/latest/action/troubleshoot'
    data = {"scheduleType": "IMMEDIATE", "type": "scheduletroubleshoot"}
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=schedule_troubleshoot_url),
                             json=data, verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed POST scheduleTroubleshoot response {} {}".format(response.status_code, response.json()))
    else:
        schedule_troubleshoot_id = response.json().get('jobHistoryUuid')
        print('Troubleshoot job scheduled successfully : {}'.format(schedule_troubleshoot_id))
    return schedule_troubleshoot_id


def get_troubleshoot_job(host, port, access_token, job_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a troubleshoot job GET request to determine the status of a troubleshoot task.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param job_id: unique identifier for job task
    :return: status of the job and name of the troubleshoot file. Filename is valid iff status = success.
    """
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    status = None
    status_message = None
    deploy_url = 'api/fdm/latest/managedentity/jobs/troubleshootjob'
    response = requests.get(
        'https://{host}:{port}/{url}/{job_id}'.format(host=host, port=port, url=deploy_url, job_id=job_id),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET job history response {} {}".format(response.status_code, response.json()))
    else:
        status = response.json().get('status')
        status_message = response.json().get('statusMessage')
        print("GET job history status: {}".format(status))
    return (status, status_message)


def download_troubleshoot(host, port, access_token, filename):
    """
    Requires Python v3.0 or greater and requests lib.
    Send a download troubleshoot POST request to obtain a troubleshoot file.
    The downloaded troubleshoot filename will consist of the troubleshoot job id followed
    by '-troubleshoot.tar.gz'.
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH token for device access
    :param filename" local file where the troubleshoot data will be stored
    """
    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Authorization": "Bearer {}".format(access_token)
    }
    indx = filename.index("-troubleshoot.tar.gz")
    job_id = filename[0:indx]
    download_troubleshoot_url = 'api/fdm/latest/action/downloadtroubleshoot'
    with requests.get(
            'https://{host}:{port}/{url}/{job_id}'.format(host=host, port=port, url=download_troubleshoot_url,
                                                          job_id=job_id),
            verify=False, headers=headers, stream=True) as response:
        response.raise_for_status()
        with open(filename, 'wb') as out_file:
            i = 0
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    if not i % 10:
                        print(".", end='', flush=True)
                    i = i + 1
                    out_file.write(chunk)
            print("Troubleshoot file downloaded successfully: {} {}".format(job_id, filename))
