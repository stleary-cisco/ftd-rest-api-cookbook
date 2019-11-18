import json
from datetime import datetime

import requests


def get_license_registration_jobs(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a  GET request to obtain License Registration jobs
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    """
    license_registrations_path = "api/fdm/latest/jobs/licenseregistrations"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token)
    }
    params = {"limit": "9999"}

    url = "https://{host}:{port}/{url}".format(host=host, port=port, url=license_registrations_path)
    print("Send a GET request to url: {}".format(url))
    response = requests.get(url, params=params, verify=False, headers=headers)

    if response.status_code != 200:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed to GET license registration jobs.")

    print(json.dumps(response.json(), indent=2))
    return response.json()["items"]


def get_last_smart_license_registration_job_status(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Returns a status of the last Smart License Registration job
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    """
    jobs = get_license_registration_jobs(host, port, access_token)
    last_job = None
    last_timestamp = 0
    for job in jobs:
        timestamp = datetime.strptime(job["startDateTime"], "%Y-%m-%d %H:%M:%SZ").timestamp()
        if job["jobName"] == "Cisco Smart Software Manager Registration" and timestamp > last_timestamp:
            last_timestamp = timestamp
            last_job = job

    if last_job is None:
        raise Exception("Smart License Registration job not found")

    print(json.dumps(last_job, indent=2))
    return last_job["status"]


def get_last_smart_license_unregistration_job_status(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Returns a status of the last Smart License Un-registration job
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    """
    jobs = get_license_registration_jobs(host, port, access_token)
    last_job = None
    last_timestamp = 0
    for job in jobs:
        timestamp = datetime.strptime(job["startDateTime"], "%Y-%m-%d %H:%M:%SZ").timestamp()
        if job["jobName"] == "Cisco Smart Software License Un-registration" and timestamp > last_timestamp:
            last_timestamp = timestamp
            last_job = job

    if last_job is None:
        raise Exception("Smart License Un-registration job not found")

    print(json.dumps(last_job, indent=2))
    return last_job["status"]
