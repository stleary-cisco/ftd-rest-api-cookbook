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
import json


def get_smart_agent_connections(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a GET request to obtain Smart Agent connections
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    """
    smart_agent_connections_path = "api/fdm/latest/license/smartagentconnections"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }

    url = "https://{host}:{port}/{url}".format(host=host, port=port, url=smart_agent_connections_path)
    print("Send a GET request to url: {}".format(url))
    response = requests.get(url, verify=False, headers=headers)

    if response.status_code != 200:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed to GET Smart Agent Connections.")
    else:
        print(json.dumps(response.json(), indent=2))

    return response.json()["items"]


def post_smart_agent_connection(host, port, access_token, smart_agent_connection):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a POST request to start Smart License Registration job
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :param smart_agent_connection: object representing  Smart Agent Connection model
    """
    smart_agent_connections_path = "api/fdm/latest/license/smartagentconnections"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json"
    }

    url = "https://{host}:{port}/{url}".format(host=host, port=port, url=smart_agent_connections_path)
    print("Send a POST request to url: {}".format(url))
    response = requests.post(url, data=json.dumps(smart_agent_connection), verify=False, headers=headers)

    if response.status_code != 200:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed to POST Smart Agent Connection: {}".format(json.dumps(smart_agent_connection)))

    print(json.dumps(response.json(), indent=2))
    print("Smart License Registration job started successfully.")

    return response.json()


def delete_smart_agent_connection(host, port, access_token, obj_id):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a DELETE request to start Smart License Un-registration job
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :param obj_id: id of smartagentconnection object to delete
    """
    smart_agent_connections_path = "api/fdm/latest/license/smartagentconnections"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json"
    }

    url = "https://{host}:{port}/{url}/{objid}".format(host=host, port=port, url=smart_agent_connections_path,
                                                       objid=obj_id)
    print("Send a DELETE request to url: {}".format(url))
    response = requests.delete(url, verify=False, headers=headers)

    if response.status_code != 204:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed DELETE Smart Agent Connection.")


def get_smart_agent_statuses(host, port, access_token):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a GET request to obtain Smart Agent statuses
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    """
    smart_agent_statuses_path = "api/fdm/latest/license/smartagentstatuses"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
    }

    url = "https://{host}:{port}/{url}".format(host=host, port=port, url=smart_agent_statuses_path)
    print("Send a GET request to url: {}".format(url))
    response = requests.get(url, verify=False, headers=headers)

    if response.status_code != 200:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed to GET Smart Agent Statuses.")
    else:
        print(json.dumps(response.json(), indent=2))

    return response.json()["items"]


def post_smart_agent_sync_requests(host, port, access_token, smart_agent_sync_request):
    """
    Requires Python v3.0 or greater and requests lib.
    Sends a POST request to sync Smart Agent
    :param host: ftd host address
    :param port: ftd port
    :param access_token: OAUTH access token
    :param smart_agent_sync_request: object representing Smart Agent Sync Request model
    """
    smart_agent_sync_requests_path = "api/fdm/latest/license/smartagentsyncrequests"
    headers = {
        "Accept": "application/json",
        "Authorization": "Bearer {}".format(access_token),
        "Content-Type": "application/json"
    }

    url = "https://{host}:{port}/{url}".format(host=host, port=port, url=smart_agent_sync_requests_path)
    print("Send a POST request to url: {}".format(url))
    response = requests.post(url, data=json.dumps(smart_agent_sync_request), verify=False, headers=headers)

    if response.status_code != 200:
        print("Failed with status {}: {}".format(response.status_code, json.dumps(response.json(), indent=2)))
        raise Exception("Failed to POST Smart Agent Sync Request: {}".format(json.dumps(smart_agent_sync_request)))

    print(json.dumps(response.json(), indent=2))
    print("Smart Agent Sync request is successfully sent.")

    return response.json()
