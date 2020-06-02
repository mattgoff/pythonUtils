import requests
import urllib3
import pprint
import json

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

clashKeyGmail = "clash key"
authorToken = "Bearer {}".format(clashKeyGmail)

headers = {
    "Accept": "application/json",
    "Authorization": authorToken,
}

sendUrl = "http://www.goff.us/api/coc"
auth_token = "bearer tokey"
head = {'Content-Tyep': "application/json", 'Authorization': 'token {}'.format(auth_token)}

fulldict = {
    "warData": {},
    "playerData": {},
    "clanData": {},
}

apiURLClan = "https://api.clashofclans.com/v1/clans/%2329VG0828V"
clanResponse = requests.get(apiURLClan, headers=headers, verify=False)
fulldict["clanData"] = clanResponse.json()

playerList = []
for player in fulldict['clanData']['memberList']:
    playerList.append("%23" + player['tag'].lstrip("#"))

for player in playerList:
    apiURlPlayer = "https://api.clashofclans.com/v1/players/" + player
    playerResponse = requests.get(apiURlPlayer, headers=headers, verify=False)
    fulldict["playerData"][player] = playerResponse.json()

apiURLWarLog = "https://api.clashofclans.com/v1/clans/%2329VG0828V/warlog"
warlogResponse = requests.get(apiURLWarLog, headers=headers, verify=False)
fulldict["warData"] = warlogResponse.json()

sendResponse = requests.post(sendUrl, headers=head, json=fulldict)
sendRep = sendResponse.content
