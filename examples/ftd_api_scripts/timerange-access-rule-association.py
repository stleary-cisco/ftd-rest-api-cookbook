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
from ftd_api_resources.time_range_access_rule_association_utils import get_all_access_rules, \
    post_access_rule, update_access_rule, get_access_rule
from ftd_api_resources.timerange_utils import post_time_range
from ftd_api_resources.access_token import get_access_token


def timerange_access_rule_association_actions(host, port, user, passwd, parent_policy_id):
    """
    End to end example of code that updates an access rule.
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
    access_rules = get_all_access_rules(host, port, access_token, parent_policy_id)
    if not access_rules:
        print('Unable to get access rule')
        return False
    tro = {
        "name": "TRO_For_Python_Request_Test_6.6.0_1",
        "description": "Creating Time Range",
        "effectiveStartDateTime": "2020-07-24T12:08",
        "effectiveEndDateTime": "2020-07-28T12:08",
        "recurrenceList": [
            {
                "recurrenceType": "DAILY_INTERVAL",
                "days": ["MON", "TUE", "FRI"],
                "dailyStartTime": "08:00",
                "dailyEndTime": "09:00",
                "type": "recurrence"
            },
            {
                "recurrenceType": "RANGE",
                "rangeStartTime": "09:00",
                "rangeEndTime": "11:00",
                "rangeStartDay": "MON",
                "rangeEndDay": "TUE",
                "type": "recurrence"
            }
        ],
        "type": "timerangeobject"
    }
    time_range = post_time_range(host, port, access_token, tro)
    if not time_range:
        print('Unable to create time range object')
        return False
    access_rule = {
        "name": "Test_Python_Request_For_Access_Rule_6.6.0_1",
        "sourceZones": [],
        "destinationZones": [],
        "sourceNetworks": [],
        "destinationNetworks": [],
        "sourcePorts": [],
        "destinationPorts": [],
        "timeRangeObjects": [time_range],
        "ruleAction": "TRUST",
        "eventLogAction": "LOG_BOTH",
        "identitySources": [],
        "users": [],
        "logFiles": "false",
        "destinationDynamicObjects": [],
        "sourceDynamicObjects": [],
        "type": "accessrule"
    }
    access_rule = post_access_rule(host, port, access_token, access_rule, parent_policy_id)
    if not access_rule:
        print('Unable to create access rule')
        return False
    access_rule_update = {
        "version": access_rule['version'],
        "name": "Test_Python_Request_For_Access_Rule__6.6.0_Updated_1",
        "ruleId": access_rule['ruleId'],
        "sourceZones": [],
        "destinationZones": [],
        "sourceNetworks": [],
        "destinationNetworks": [],
        "sourcePorts": [],
        "destinationPorts": [],
        "timeRangeObjects": [time_range],
        "ruleAction": "PERMIT",
        "eventLogAction": "LOG_BOTH",
        "identitySources": [],
        "users": [],
        "logFiles": "false",
        "destinationDynamicObjects": [],
        "sourceDynamicObjects": [],
        "type": "accessrule"
    }
    updated_access_rule = update_access_rule(host, port, access_token, access_rule['id'], access_rule_update,
                                             parent_policy_id)
    if not updated_access_rule:
        print('Unable to update access rule')
        return False
    access_rule = get_access_rule(host, port, access_token, updated_access_rule['id'], parent_policy_id)
    if not access_rule:
        print('Unable to get access rule')
        return False
    print('Access rule name is {}'.format(access_rule['name']))
    access_rule_update = {
        "version": access_rule['version'],
        "name": "Test_Python_Request_For_Access_Rule_Deleted_TRO_6.6.0_1",
        "ruleId": access_rule['ruleId'],
        "sourceZones": [],
        "destinationZones": [],
        "sourceNetworks": [],
        "destinationNetworks": [],
        "sourcePorts": [],
        "destinationPorts": [],
        "ruleAction": "PERMIT",
        "eventLogAction": "LOG_BOTH",
        "identitySources": [],
        "users": [],
        "logFiles": "false",
        "destinationDynamicObjects": [],
        "sourceDynamicObjects": [],
        "type": "accessrule"
    }
    updated_access_rule = update_access_rule(host, port, access_token,
                                             access_rule['id'], access_rule_update, parent_policy_id)
    if not updated_access_rule:
        print('Unable to update access rule')
        return False
    print('Access rule name is {}'.format(updated_access_rule['name']))
    return True


if __name__ == '__main__':

    if len(sys.argv) != 6:
        print("Usage: python cookbook_scripts/timerange-access-rule-association.py host port user passwd")
        exit(1)

    host = sys.argv[1]
    port = sys.argv[2]
    user = sys.argv[3]
    passwd = sys.argv[4]
    parent_policy_id = sys.argv[5]
    if timerange_access_rule_association_actions(host, port, user, passwd, parent_policy_id):
        exit(0)
    else:
        exit(1)
