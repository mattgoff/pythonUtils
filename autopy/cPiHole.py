# from __future__ import division
import requests
import urllib3
import json
import pdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "http://www.goff.us/api/pi"
auth_token = "BearerToken"
head = {'Content-Type': "application/json", 'Authorization': 'Bearer {}'.format(auth_token)}

body_data = {}

def send_info():
    response = requests.post(url, headers=head, verify=False, data=json.dumps(body_data))
    #pdb.set_trace()
    data = response.reason
    print(data)

def pi_hole_stats():
    pi_hole_server = "172.16.12.9"
    r = requests.get('http://' + pi_hole_server + '/admin/api.php')
    output_info = r.json()
    body_data['blocks24Hours'] = str(output_info['ads_blocked_today'])
    body_data['dnsQ24Hours'] =  str(output_info['dns_queries_today'])
    print(body_data)

pi_hole_stats()
send_info()

