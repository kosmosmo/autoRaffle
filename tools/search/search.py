from airtable_wrapper import AirtableWrapper

import time,random,json

import random

filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
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
with open(r'C:\Users\kosmo\PycharmProjects\autoRaffle\tools\search\search_file',errors="ignore") as f:
    contents = f.read()
cc_low = contents.lower()
for key,val in res.items():
    if key.lower() in cc_low:
        print (val)
