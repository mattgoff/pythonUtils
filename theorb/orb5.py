import requests
from requests.auth import HTTPBasicAuth
import pdb
import getpass
import os
import time
import json
import urllib3
import ast

urllib3.disable_warnings()

alarm_url = "alarm url"

get_dweet_url = "get url"
send_dweet_url = "send url"

# username = input("Enter OpenNMS userid: ")
# password = getpass.getpass("Enter OpenNMS password: ")
username = 'username'
password = 'password'
headers = {'Accept': 'application/json', 'cache-control': "no-cache",}

def get_alarms(username, password):
    mino_count = 0
    warn_count = 0
    crit_count = 0
    majo_count = 0
    affected_node_list = []
    alarm_response = requests.get(alarm_url, auth=(username, password), headers=headers, verify=False)
    alarm_json = alarm_response.json()
    for alarm in alarm_json['alarm']:
        if "MINOR" in alarm['severity']:
            # print(f"Warning {alarm['id']}")
            mino_count += 1
            if not alarm.get('nodeLabel') == None:
                affected_node_list.append(alarm.get('nodeLabel').split(".")[0].upper())
        if "WARNING" in alarm['severity']:
            if "authentication failure trap signifies" not in alarm['description']:
                # print(f"Warning {alarm['id']}")
                warn_count += 1
            if not alarm.get('nodeLabel') == None:
                affected_node_list.append(alarm.get('nodeLabel').split(".")[0].upper())
        if "CRITICAL" in alarm['severity']:
            # print(f"Critical {alarm['id']}")
            crit_count += 1
            affected_node_list.append(alarm.get('nodeLabel').split(".")[0].upper())
        if "MAJOR" in alarm['severity']:
            # print(f"Major {alarm['id']}")
            majo_count += 1
            try:
                affected_node_list.append(alarm.get('nodeLabel').split(".")[0].upper())
            except:
                affected_node_list.append("error")
    return [mino_count, warn_count, crit_count, majo_count, alarm_json['count'], affected_node_list]

def set_blinky(warn_count, crit_count, majo_count):
    if crit_count > 0:
        print("setting Critical")
        os.system('blink1-tool --rgb=800000')
    elif majo_count > 0:
        print("setting Major")
        os.system('blink1-tool --rgb=661900')
    elif warn_count > 0:
        print("setting Warning")
        os.system('blink1-tool --rgb=806600')
    else:
        print("setting all good")
        os.system('blink1-tool --rgb=114400')

def get_dweets():
    try:
        response = requests.get(get_dweet_url)
        dweet_data = ast.literal_eval((response.json())['with'][0]['content']['status'].replace("null", "None"))
        mino_count = dweet_data['Minors']
        warn_count = dweet_data['Warnings']
        majo_count = dweet_data['Majors']
        crit_count = dweet_data['Criticals']
        total_count = dweet_data['Total_Alarms']
        affected_node_list = dweet_data['Nodes_with_alarms']

        return (mino_count, warn_count, majo_count, crit_count, total_count, affected_node_list)
    except:
        print("error getting dweet")

loop_forever = True

while loop_forever:

    mino_count, warn_count, majo_count, crit_count, total_count, affected_node_list = get_dweets()
    print(f"Minors: {mino_count},  Warnings: {warn_count},  Majors: {majo_count}, Criticals: {crit_count}, Total Alarms: {total_count}, Nodes Warning or greater alarms: {affected_node_list}")
    set_blinky(warn_count, crit_count, majo_count)

    try:
        time.sleep(60)
    except KeyboardInterrupt:
        loop_forever = False


