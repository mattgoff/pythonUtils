import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

clashKeyGmail = "clash token"
authorToken = "Bearer {}".format(clashKeyGmail)

headers = {
    "Accept": "application/json",
    "Authorization": authorToken,
}

apiURlGmail = "https://api.clashofclans.com/v1/players/%23JLPUGJOP"
apiURLClan = "https://api.clashofclans.com/v1/clans/%2329VG0828V"
apiURLWarLog = "https://api.clashofclans.com/v1/clans/%2329VG0828V/warlog"



requestResponse = requests.get(apiURlGmail, headers=headers, verify=False)
clanResponse = requests.get(apiURLClan, headers=headers, verify=False)
warlogResponse = requests.get(apiURLWarLog, headers=headers, verify=False)
respJson = requestResponse.json()
clanJson = clanResponse.json()
warJson = warlogResponse.json()
import pprint
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(clanJson)
pp.pprint(warJson)
# import pdb; pdb.set_trace()
itemsList = ['tag', 'name','league','townHallLevel', 'expLevel', 'trophies', 'bestTrophies',
            'warStars', 'attackWins', 'defenseWins', 'versusTrophies', 'versusBattleWins', 'versusBattleWinCount', "heroes", "troops", 'spells']

if respJson.get('league', 'Empty') == "Empty":
    league = "Not Ranked"
else:
    league = respJson['league']['name']

for item in itemsList:
    if item == 'league':
        print("league{:23}{}".format(" ", league))
    elif item == 'heroes':
        print(" ")
        print("{:20}         {:18} {:6} {:5}".format(" ", "Hero", "Level", "Max"))
        print("{:29}{}".format(" ", "-----------------------------"))
        for hero in respJson[item]:
            aaa = ""
            print(f"{aaa:20}         {hero['name']:15} {hero['level']:6} {hero['maxLevel']:5}")
    elif item == 'spells':
        print(" ")
        print("{:20}         {:18} {:6} {:5}".format(" ", "Spell", "Level", "Max"))
        print("{:29}{}".format(" ", "-----------------------------"))
        for spell in respJson[item]:
            aaa = ""
            print(f"{aaa:20}         {spell['name']:15} {spell['level']:6} {spell['maxLevel']:5}")
    elif item == "troops":
        print(" ")
        print("{:20}         {:18} {:6} {:5}".format(" ", "Troop", "Level", "Max"))
        print("{:29}{}".format(" ", "-----------------------------"))
        for troop in respJson[item]:
            aaa = ""
            print(f"{aaa:20}         {troop['name']:15} {troop['level']:6} {troop['maxLevel']:5}")
    else:
        print(f"{item:20}         {respJson[item]}")
# import pdb; pdb.set_trace()
# for key, val in respJson.items():
#     print(f"{key}: {val}")
