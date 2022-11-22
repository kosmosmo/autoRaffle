import requests,time
s = requests.session()
header = {"Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,fr;q=0.6",
    "Connection": "keep-alive",
    "Content-Length": "97",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Cookie": "_ga=GA1.1.1702000957.1667878818; _ga_15YKY2QD9V=GS1.1.1667878817.1.1.1667880495.10.0.0; XSRF-TOKEN=eyJpdiI6ImZMaFh1QWlTRGxDODhZdGQ3RmU0Q3c9PSIsInZhbHVlIjoiYVprRWFENGk2djlLSkFGUVNWbnpTRU9teW52VTdCRURHYktoT3NzUS9Qa0JpVmI2a1BuQUdJbXZPQmFZdnR4M3JlK0pLdmJmUmR5K0VESk9tKzZ3YlEvblpUdnUxVElTV1ptNTVlQTVUTjBUWHo2OUFYcUIzN1E4Rm1OYkU1b2UiLCJtYWMiOiIwZWY3NTNkN2FjZWY2ZjkxYzNiZDYwNDg2NzgzYzZlOTI5Zjc1N2RkY2RmZjY4OGQ4ZTk5MWIzNTY5NWNjNjdjIiwidGFnIjoiIn0%3D; voiders_session=eyJpdiI6IndCUFBhSmc2dGhxL042emVhNWJSWUE9PSIsInZhbHVlIjoicllsakpqWTF4RExaYnN5MHVwSG1YWTNpRUxPanlMdFd6QXhxTzFxRzBDNFZOc0F4aVo5ak0wTVc5RGg5VnhJZ0p4TnExUjVXanBKb3hHR2RFdEhZa0lrbVRiY3J1YmJwNDhGTEVpOSszbkRSVTZsUTIrUGRuNXhVZ2ZpejlVZWQiLCJtYWMiOiIxZmU4ZjdjN2Y0MTc0MjkxNDBmZTU0ODRjYjM2NjhkNGYxMWRmNzBiZTY3MDI1NWQ5MGE4NTgwYTY0MTM4YjJhIiwidGFnIjoiIn0%3D",
    "Host": "voiders.gg",
    "Origin": "https://voiders.gg",
    "Referer": "https://voiders.gg/wallet_checker",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest",
    "sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows"}

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


url =  "https://mainnet.infura.io/v3/adfeab0dfdc44dbd8aac83b05c113d9e"

import json
def get_airtable():
    index_list = at_obj.get_all("emails").get('records')
    for item in index_list:
        fields = item.get('fields')
        rid = item.get('id')
        ID = fields.get("ID")
        wallet = fields.get("wallet",'')
        wallet_mint = fields.get("wallet_mint",'')

        if wallet_mint:
            data =
            a = s.post("https://whitelist.pams.art/livewire/message/guest.contact-form", json={"jsonrpc":"2.0","id":2,"method":"eth_call","params":[{"data":"0x68428a1b","to":wallet_mint},"latest"]})
            print (ID,a.text)
        time.sleep(0.1)

get_airtable()