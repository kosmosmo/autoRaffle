import requests,time
s = requests.session()
header = {
"accept": "application/json",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,fr;q=0.6",
"content-length": "60",
"content-type": "application/json; charset=utf-8",
"cookie": "__cf_bm=PXj.y85i3YX78C1KB74JpL7mCQSE9w.30bx3BDH2TDg-1669663236-0-AYmbKWKvUJxT9X1KGkzVyjzam2yWM464qK/rwGZthgBTkDAVM1YVQ/9tSLg/sPbJW6eBNkMhQzrJUmtoLoksW595yW6LTKIfVjvQNf+8rLMKlTr++q+JFbVppqxnMM7CUjUXkRe6UsdcqUbkBZtqpCM=; SERVERID=1dff1738c157dd4858c0460923139431|1669663253|1669663231",
"origin": "https://www.heyreap3r.com",
"referer": "https://www.heyreap3r.com",
"sec-ch-ua": '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
"sec-ch-ua-mobile": "?0",
"sec-ch-ua-platform": "Windows",
"sec-fetch-dest": "empty",
"sec-fetch-mode": "cors",
"sec-fetch-site": "same-origin",
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}

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


url =  "https://www.heyreap3r.com/heyreap3r/getAddressWhitelist"

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
            data ={"userAddress": wallet_mint}
            a = s.post("https://whitelist.pams.art/livewire/message/guest.contact-form", json={"fingerprint":{"id":"aaWGGzAXEGMzlBnOZdhb","name":"guest.contact-form","locale":"en","path":"/","method":"GET","v":"acj"},"serverMemo":{"children":[],"errors":[],"htmlHash":"ed447378","data":{"address":wallet_mint,"email":"","message":""},"dataMeta":[],"checksum":"b51b33806316f9a0b20b447909669165b25d2e70c00a94ed505ce5aa67c9475f"},"updates":[{"type":"callMethod","payload":{"id":"uslck","method":"submit","params":[]}}]}, headers={"x-csrf-token": "2FHNvRyKf7Vk7bNBm2TBUdHbb5UzZ5pq4cNcEpqF", "x-livewire": "true"})
            print (ID,a.text)
        time.sleep(0.1)

get_airtable()