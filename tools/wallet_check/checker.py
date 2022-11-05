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


url = "https://www.astersnft.com/api/contract/"


def get_airtable():
    index_list = at_obj.get_all("emails").get('records')
    for item in index_list:
        fields = item.get('fields')
        ID = fields.get("ID")
        wallet = fields.get("wallet",'')
        wallet_mint = fields.get("wallet_mint",'')
        if wallet:
            wl = requests.get(url + wallet_mint).text
            if wl != '""':
                print( wl + ":" + ID)
        if wallet_mint:
            wl_mint = requests.get(url + wallet_mint).text
            if wl_mint != '""':
                print (wl_mint + ":" + ID)

def get_local():
    with open(root_path + 'tools\\wallet_check\\wallet') as f:
        lines = f.readlines()
    for item in lines:
        wallet = item.replace("\n",'')
        if wallet:
            wl_mint = requests.get(url + wallet).text
            if wl_mint != '""':
                print (wallet)

url2 = "https://eth-mainnet.g.alchemy.com/v2/h3_7LGA7ul51x4G1lcVPuG2EKZf9ZhfK"
data = {"jsonrpc":"2.0","id":3,"method":"eth_call","params":[{"data":"0x6caede3d","to":"0xd919dc6ed1091bc0a60f523024385a799ad31d3e"},"latest"]}
a = requests.post(url2,data = data)
print (a.text)