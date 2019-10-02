import time
import requests


def get_pending_changes(host: str, port: str, headers: {}) -> bool:
    """
    Sends a GET rquest to obtain the pending changes from the FTD device
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :return: True if changes are pending, otherwise False
    """
    pending_changes_url = 'api/fdm/latest/operational/pendingchanges'
    response = requests.get('https://{host}:{port}/{url}'.format(host=host, port=port, url=pending_changes_url),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET pending changes response {}".format(response.status_code))
    changes_found = True if response.json().get('items') else False
    print("GET pending changes found: {}".format(str(changes_found)))
    return changes_found


def post_deployment(host: str, port: str, headers: {}) -> str:
    """
    Send a deployment POST request
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :return: unique id for the deployment task
    """
    deploy_url = 'api/fdm/latest/operational/deploy'
    id = None
    response = requests.post('https://{host}:{port}/{url}'.format(host=host, port=port, url=deploy_url), verify=False,
                             headers=headers)
    if response.status_code != 200:
        print("Failed POST deploy response {}".format(response.status_code))
    else:
        print("POST deployment successful")
        id = response.json().get('id')
    return id


def get_deployment_status(host: str, port: str, headers: {}, id: str):
    """
    Wait for a deployment to complete
    :param host: ftd host address
    :param port: ftd port
    :param headers: HTTP request headers
    :param id: unique identifier for deployment task
    """
    deploy_url = 'api/fdm/latest/operational/deploy'
    state = None
    response = requests.get('https://{host}:{port}/{url}/{id}'.format(host=host, port=port, url=deploy_url, id=id),
                            verify=False, headers=headers)
    if response.status_code != 200:
        print("Failed GET deploy response {}".format(response.status_code))
    else:
        state =  response.json().get('state')
        print("GET Deployment state: {}".format(state))
    return state
