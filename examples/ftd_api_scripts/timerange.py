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

from ftd_api_resources.timerange_utils import get_all_time_range, post_time_range, update_time_range, get_time_range, delete_time_range
from ftd_api_resources.access_token import get_access_token

def main():
    """
    End to end example of code that updates an intrusion rule.
    Requires Python v3.0 or greater and the reqeusts library.
    You must update the values for host, port, user, and password to connect to your device.
    """
    host = 'u32c01p10-vrouter.cisco.com'
    port = '20248'
    user = 'admin'
    passwd = 'Cisco@123'
    access_token = get_access_token(host, port, user, passwd)
    if not access_token:
        print("Unable to obtain an access token. Did you remember to set host, port, user, and password?")
        return
    time_range = get_all_time_range(host, port, access_token)
    if not time_range:
        print('Unable to get time range')
        return
    tro = {
    "name": "TRO_Python_Request_Test_2",
    "description": "creating Time Range",
    "effectiveStartDateTime": "2020-07-24T12:08",
    "effectiveEndDateTime": "2020-07-28T12:08",
    "recurrenceList": [
    {
      "recurrenceType": "DAILY_INTERVAL",
      "days": ["MON","TUE","FRI"],
      "dailyStartTime": "08:00",
      "dailyEndTime": "09:00",
      "type" : "recurrence"
    },
    {
      "recurrenceType": "RANGE",
      "rangeStartTime": "09:00",
      "rangeEndTime": "11:00",
      "rangeStartDay": "MON",
      "rangeEndDay": "TUE",
      "type" : "recurrence"
    }
  ],
  "type": "timerangeobject"
  }
    time_range = post_time_range(host, port, access_token, tro)
    if not time_range:
        print('Unable to create time range object')
        return
    tro_update = {
    'version': time_range['version'],
    "name": "TRO_Python_Request_Test_Name_updated_2",
    "description": "editing Time Range",
    "effectiveStartDateTime": "2019-11-24T12:08",
    "effectiveEndDateTime": "2019-12-28T12:08",
    "recurrenceList": [
    {
      "recurrenceType": "DAILY_INTERVAL",
      "days": ["MON","TUE","FRI"],
      "dailyStartTime": "08:00",
      "dailyEndTime": "09:00",
      "type" : "recurrence"
    },
    {
      "recurrenceType": "RANGE",
      "rangeStartTime": "09:00",
      "rangeEndTime": "11:00",
      "rangeStartDay": "MON",
      "rangeEndDay": "TUE",
      "type" : "recurrence"
    }
  ],
  "type": "timerangeobject"
    }
    updated_tro = update_time_range(host, port, access_token, time_range['id'], tro_update)
    if not updated_tro:
        print('Unable to update time range object')
        return
    tro = get_time_range(host, port, access_token, updated_tro['id'])
    if not tro:
        print('Unable to get time range object')
        return
    print('TRO name is {}'.format(tro['name']))
    returnCode = delete_time_range(host, port, access_token, tro['id'])
    if not returnCode:
        print('Unable to delete time range object')
        return

if __name__ == '__main__':
    main()