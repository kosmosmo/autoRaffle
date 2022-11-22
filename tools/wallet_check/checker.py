import requests
import discum,json,pprint
from airtable_wrapper import AirtableWrapper

root_path = "C:\\Users\\kosmo\\PycharmProjects\\autoRaffle\\"

def _get_keys():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
keys = _get_keys()
key = keys['key']
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)


url =  "https://chilltuna.club/api/mintRole?address="


def get_airtable():
    index_list = at_obj.get_all("emails").get('records')
    for item in index_list:
        fields = item.get('fields')
        ID = fields.get("ID")
        wallet = fields.get("wallet",'')
        rid =  item.get('id')
        wallet_mint = fields.get("wallet_mint",'')

        if wallet_mint:
            wl_mint = requests.get(url + wallet_mint).text
            print (ID,wl_mint)
            #at_obj.update("temp",rid,{"proof":wl_mint})

def get_local():
    with open(root_path + 'tools\\wallet_check\\wallet') as f:
        lines = f.readlines()
    for item in lines:
        wallet = item.replace("\n",'')
        if wallet:
            wl_mint = requests.get(url + wallet).text
            if wl_mint != '""':
                print (wallet)
get_airtable()
