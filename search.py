from airtable_wrapper import AirtableWrapper

import time,random,json

import random

filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
root_path = r"C:\Users\kosmo\PycharmProjects\autoRaffle"
def _get_key():
    f = open(root_path + '\key.json')
    data = json.load(f)
    return data
data = _get_key()
at_keys = data["key"]
machine_name = data.get('name','All')
profiles = data.get("profile",[])
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",at_keys)

res = {}
wals = at_obj.get_all("emails").get('records')
for w in wals:
    fields = w.get('fields')
    wallet1 = fields.get("wallet","")
    wallet2 = fields.get("wallet_mint","")
    name = fields.get("ID","")
    if wallet1:
        res[wallet1] = name
    if wallet2:
        res[wallet2] = name + "2"
with open(root_path+'\search\\search_file') as f:
    contents = f.read()

for key,val in res.items():
    if key in contents:
        print (val)