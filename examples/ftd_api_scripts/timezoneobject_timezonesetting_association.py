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
from ftd_api_resources.timezoneobject_timezonesetting_association_utils import get_all_timezone_setting, \
    update_timezone_setting, get_timezone_setting
from ftd_api_resources.timezone_utils import post_time_zone
from ftd_api_resources.access_token import get_access_token


def timezoneobject_timezonesetting_associated_actions(host, port, user, passwd):
    """
    End to end example of code that updates the timezone-setting.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """

    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
    timezone_setting = get_all_timezone_setting(host, port, access_token)
    if not timezone_setting:
        print('Unable to get timezone setting')
        return
    tzo = {
        "name": "Tzo_Dst_Recurrence_14",
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
        return

    updated_tzs = {
        "version": timezone_setting['version'],
        "name": "TZS",
        "description": "TestTimeZoneSetting",
        "timeZoneObject": time_zone,
        "type": "timezonesetting"
    }
    updated_tzs = update_timezone_setting(host, port, access_token, timezone_setting['id'], updated_tzs)
    if not updated_tzs:
        print('Unable to update timezone setting')
        return
    tzs = get_timezone_setting(host, port, access_token, updated_tzs['id'])
    if not tzs:
        print('Unable to get timezone setting')
        return
    print('TimeZone Setting name and Id are {} {}'.format(tzs['name'], tzs['id']))


if __name__ == '__main__':

    if len(sys.argv) != 5:
        print("Usage: python cookbook_scripts/timezoneobject_timezonesetting_association.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    timezoneobject_timezonesetting_associated_actions(host, port, user, passwd)
