from __future__ import print_function
from typing import List
import os.path
import pprint
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googles_apis import google_apis
import sys
import os
import base64,re
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "\\util\\")
from airtable_wrapper import AirtableWrapper
import cloudscraper
import json
import utils as _u
import time
import datetime,discum,re
from datetime import datetime as dt
root_path = "C:\\Users\\kosmo\\PycharmProjects\\autoRaffle\\"
def _get_keys():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
keys = _get_keys()
bearer_token = keys["bearer_token"]
at_key = keys['key']
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",at_key)

def join_dc_list(code):
    wallets_map = {}
    wallets = at_obj.get_all("emails").get('records')
    for wal in wallets:
        fields = wal.get('fields')
        name = fields.get("ID", '')
        dc_token = fields.get("discord token", '')
        wallets_map[name] = dc_token
        if dc_token:
            bot = discum.Client(token=dc_token, log=False)
            res = bot.joinGuild(code)
            print (name)
            print (res.text)

#join_dc_list('e4c')
bot = discum.Client(token='MTAxMjA1NzQzMjI0NTE1Nzg4OQ.GYJ-8D.uGzcZPn5dp9YIlf9YjHaKGIPgZ0BNk9ktS6p1w', log=False)
res = json.loads(bot.joinGuild('e4c').text)
pprint.pprint(res)