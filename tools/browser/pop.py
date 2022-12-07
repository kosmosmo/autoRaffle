from airtable_wrapper import AirtableWrapper

import time,random,json

import random
import webbrowser

root_path = r"/"
def _get_key():
    f = open(r'C:\Users\kosmo\PycharmProjects\autoRaffle\key.json')
    data = json.load(f)
    return data
data = _get_key()
at_keys = data["key"]
machine_name = data.get('name','All')
profiles = data.get("profile",[])
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",at_keys)

profile_index = {}
wals = at_obj.get_all("emails").get('records')
for w in wals:
    fields = w.get('fields')
    wallet2 = fields.get("wallet_mint","")
    name = fields.get("ID","")
    pid = fields.get("profile","")
    if pid and name:
        profile_index[name.lower()] = pid

def pop(rid,url=""):
    cur_wallets = at_obj.get("projects",rid).get("fields",{}).get("wallets",[])
    for wallet in cur_wallets:
        if wallet.lower() in profile_index:
            profile = ' --profile-directory="Profile {}"'.format(profile_index[wallet.lower()])
            chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s' + profile
            webbrowser.get(chrome_path).open_new(url)
        else:
            print ('skip ' + wallet.lower())

pop("recQXY8gscRPUTPA1",'https://www.hungryhamster.club/')