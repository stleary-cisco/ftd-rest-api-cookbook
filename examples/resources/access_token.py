import requests


def get_access_token(host: str, port: str, user: str, passwd: str, headers: {}) -> str:
    """
    Login to FTD device and obtain an access token. The access token is required so that the user can
    connect to the device to send REST API requests.
    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :param headers: HTTP request headers
    :return: OAUTH access token
    """
    access_token = None
    requests.packages.urllib3.disable_warnings()
    payload = '{{"grant_type": "password", "username": "{}", "password": "{}"}}'.format(user, passwd)
    auth_headers = {**headers, 'Authorization': 'Bearer '}
    try:
        response = requests.post("https://{}:{}/api/fdm/latest/fdm/token".format(host, port),
                             data=payload, verify=False, headers=auth_headers)
        if response.status_code == 200:
            access_token = response.json().get('access_token')
            print("Login successful, access_token obtained")
    except Exception as e:
        print("Unable to POST access token request: {}".format(str(e)))

    return access_token
