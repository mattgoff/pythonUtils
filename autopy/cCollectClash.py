import requests
import urllib3
import pprint
import json
import pdb

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

clashKeyGmail = "clash key"
authorToken = "Bearer {}".format(clashKeyGmail)

headers = {
    "Accept": "application/json",
    "Authorization": authorToken,
}

sendUrl = "https://www.goff.us/api/coc"
auth_token = "Bearer Token"
head = {'Content-Type': "application/json", 'Authorization': 'Bearer {}'.format(auth_token)}

clandict = {
    "warData": {},
    "playerData": {},
    "clanData": {},
}

playerdict = {}

apiURLClan = "https://api.clashofclans.com/v1/clans/%2329VG0828V"
clanResponse = requests.get(apiURLClan, headers=headers, verify=False)
if clanResponse.status_code == 403:
  print(ClanResponse.reason)

clandict["clanData"] = clanResponse.json()

playerList = []
for player in clandict['clanData']['memberList']:
    playerList.append("%23" + player['tag'].lstrip("#"))

for player in playerList:
    apiURlPlayer = "https://api.clashofclans.com/v1/players/" + player
    playerResponse = requests.get(apiURlPlayer, headers=headers, verify=False)
    postData = requests.post(sendUrl, headers=head, verify=False, json=playerResponse.json())
    print(postData.reason)

