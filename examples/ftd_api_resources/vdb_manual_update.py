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

import requests


def fetch_vdb_version(host, port, auth_token):
    """
    Requires Python v3.0 or greater and the requests library.
    Sends a GET request to obtain the System Information from the FTD device
    Then returns the current VDB version in the format ###
    :param host: ftd host address
    :param port: ftd port
    :param auth_token: authentication token for API user
    :return: String, current VDB version
    """

    # assemble and send request for system information
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(auth_token)
    }
    requests.packages.urllib3.disable_warnings()
    system_info_url = 'api/fdm/v5/operational/systeminfo/default'
    response = requests.get('https://{host}:{port}/{url}'.format(host=host, port=port, url=system_info_url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET System Information response code: {}".format(response.status_code))
        print("Failed GET System Information response information: {}".format(response.json().get('message')))
        return -1

    # get the child object with VDB information
    system_information = response.json()
    vdb_version = system_information.get('vdbVersion')
    if not vdb_version:
        # VDB information was not found; return -1
        print('System Information did not include vdb information.')
        return -1

    # get the field with VDB version
    vdb_current_version = vdb_version.get('vdbCurrentVersion')
    print('Found vdb version: {}'.format(vdb_current_version))
    return vdb_current_version


def fetch_all_vdb_jobs(host, port, auth_token):
    """
    Requires Python v3.0 or greater and the requests library.
    Sends a GET request to obtain the VDB update jobs information from the FTD device
    Then returns the list of VDB update jobs starting with the most recent
    :param host: ftd host address
    :param port: ftd port
    :param auth_token: authentication token for API user
    :return: list of VDB update jobs starting with the most recent
    """

    # assemble and send request for all VDB update jobs
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(auth_token)
    }
    requests.packages.urllib3.disable_warnings()
    vdb_update_jobs_url = 'api/fdm/v5/jobs/vdbupdates'
    # get the most recent job first
    query_params = 'sort=-startDateTime'
    response = requests.get(
        'https://{host}:{port}/{url}?{query_params}'.format(host=host, port=port, url=vdb_update_jobs_url,
                                                            query_params=query_params), verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET VDB update jobs. Response code: {}.".format(response.status_code))
        print('Failed GET VDB update jobs. Response message: {}'.format(response.json().get('message')))
        return None

    # return the relevant object list
    jobs_response = response.json()
    jobs_list = jobs_response.get('items')
    return jobs_list


def fetch_vdb_job_by_id(host, port, auth_token, uuid):
    """
    Requires Python v3.0 or greater and the requests library.
    Sends a GET request to obtain the job information from the FTD device for the given uuid
    Then returns the VDB update job associated with the uuid
    :param host: ftd host address
    :param port: ftd port
    :param uuid: UUID of the desired job
    :param auth_token: authentication token for API user
    :return: JSON object associated with the requested VDB update job
    """

    # assemble and send request for the GeoDB update job associated with the given uuid
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(auth_token)
    }
    requests.packages.urllib3.disable_warnings()
    vdb_update_jobs_url = 'api/fdm/v5/jobs/vdbupdates/'
    response = requests.get(
        'https://{host}:{port}/{url}/{uuid}'.format(host=host, port=port, url=vdb_update_jobs_url, uuid=uuid),
        verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET VDB update job. Response code: {}.".format(response.status_code))
        print('Failed GET VDB update job. Response message: {}'.format(response.json().get('message')))
        return None

    # return the object representing the requested update job
    job_response = response.json()
    return job_response


def delete_vdb_update_job_by_id(host, port, auth_token, uuid):
    """
    Requires Python v3.0 or greater and the requests library.
    Sends a DELETE request to remove jobs information from the FTD device
    :param host: ftd host address
    :param port: ftd port
    :param uuid: UUID of the desired job
    :param auth_token: authentication token for API user
    :return: JSON object associated with the requested VDB update job
    """

    # assemble and send request to delete the VDB update job associated with the given uuid
    headers = {
        'Accept': 'application/json',
        'Authorization': 'Bearer {}'.format(auth_token)
    }
    requests.packages.urllib3.disable_warnings()
    vdb_update_jobs_url = 'api/fdm/v5/jobs/vdbupdates/'
    response = requests.delete(
        'https://{host}:{port}/{url}/{uuid}'.format(host=host, port=port, url=vdb_update_jobs_url, uuid=uuid),
        verify=False, headers=headers)
    if response.status_code != 204:
        print('Failed DELETE VDB update job history. Response code: {}.'.format(response.status_code))
        print('Failed DELETE VDB update job history. Response message: {}'.format(response.json().get('message')))
    else:
        print('Successfully removed VDB update job history.')

    return response.status_code


def send_vdb_update_file(host, port, auth_token, path_to_update_file):
    """
    Requires Python v3.0 or greater and the requests library.
    Sends a POST request to upload the VDB update file.
    :param host: ftd host address
    :param port: ftd port
    :param auth_token: authentication token for API user
    :param path_to_update_file: path to file to upload
    :return: HTTP response status code
    """
    with open(path_to_update_file, 'rb') as update_file:
        print('Starting upload. Please wait.')

        # assemble and send the upload request
        headers = {
            'Accept': 'application/json',
            'Authorization': 'Bearer {}'.format(auth_token)
        }
        payload = {
            'fileToUpload': update_file
        }
        upload_vdb_update_url = 'api/fdm/v5/action/updatevdbfromfile'
        requests.packages.urllib3.disable_warnings()
        response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=upload_vdb_update_url),
                                 verify=False, headers=headers, files=payload)

        if response.status_code != 200:
            print('Failed POST upload VDB update. Response code: {}.'.format(response.status_code))
            print('Failed POST upload VDB update. Response message: {}'.format(response.json().get('message')))
        else:
            print('Successfully uploaded file! An update job has been scheduled. See VDB jobs for more information.')

        return response.status_code
