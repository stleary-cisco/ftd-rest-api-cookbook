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

import sys
from ftd_api_resources.timezone_utils import get_all_time_zones, post_time_zone, update_time_zone, get_time_zone, \
    delete_time_zone
from ftd_api_resources.access_token import get_access_token


def time_zone_actions(host, port, user, passwd):
    """
    End to end example of code that updates a time-zone object.
    Requires Python v3.0 or greater and the reqeusts library.
    :param host: ftd host address
    :param port: ftd port
    :param user: login user name
    :param passwd: login password
    :return: True if successful, otherwise False
    """

    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return False
    time_zones = get_all_time_zones(host, port, access_token)
    if not time_zones:
        print('Unable to get time zones')
        return False
    tzo = {
        "name": "TZO1",
        "timeZoneId": "Asia/Kolkata",
        "description": "TestTimeZone",
        "dstDayRecurrence": {
            "startMonth": "JUN",
            "startWeek": "FIRST",
            "startDayOfWeek": "SAT",
            "startTime": "09:00",
            "endMonth": "JUN",
            "endWeek": "SECOND",
            "endDayOfWeek": "SAT",
            "endTime": "11:01",
            "offset": 45,
            "type": "daylightsavingdayrecurrence"
        },
        "type": "timezoneobject"
    }

    time_zone = post_time_zone(host, port, access_token, tzo)
    if not time_zone:
        print('Unable to create time zone object')
        return False
    tz_update = {
        'version': time_zone['version'],
        "name": "TZO1",
        "timeZoneId": "Asia/Kolkata",
        "description": "TestTimeZone",
        "dstDateRange": {
            "startDateTime": "2020-08-19T15:22:10",
            "endDateTime": "2020-09-20T18:16",
            "type": "daylightsavingdaterange"
        },
        "type": "timezoneobject"
    }
    updated_tz = update_time_zone(host, port, access_token, time_zone['id'], tz_update)
    if not updated_tz:
        print('Unable to update time zone object')
        return False
    tzo = get_time_zone(host, port, access_token, updated_tz['id'])
    if not tzo:
        print('Unable to get time zone object')
        return False
    print('TimeZone Object name is {}'.format(tzo['name']))
    returnCode = delete_time_zone(host, port, access_token, tzo['id'])
    if not returnCode:
        print('Unable to delete time zone object')
        return
    return True


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("Usage: python ftd_api_scripts/timezone.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    if time_zone_actions(host, port, user, passwd):
        exit(0)
    else:
        exit(1)
