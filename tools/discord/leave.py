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

def update_dc_list():
    discord_map = {}
    discords = at_obj.get_all("discord").get('records')
    for wal in discords:
        rid = wal.get('id')
        fields = wal.get('fields')
        dc_id = fields.get("id", '')
        dc_wallets = fields.get("wallets", [])
        discord_map[dc_id] = {'rid':rid,
                              'wallets':dc_wallets}

    wallets = at_obj.get_all("emails").get('records')
    for wal in wallets:
        fields = wal.get('fields')
        name = fields.get("ID", '')
        rrid =  wal.get('id')
        print (name)
        dc_token = fields.get("discord token", '')
        if dc_token:
            bot = discum.Client(token=dc_token, log=False)
            dc_list = bot.getGuilds()
            dc_list = json.loads(dc_list.text)
            dc_count = len(dc_list)
            at_obj.update("emails",rrid,{"dc count": dc_count})
            for item in dc_list:
                dc_id = item.get("id")
                dc_name = item.get("name")
                dc_icon = item.get('icon')
                if dc_id not in discord_map:
                    img_url = "https://cdn.discordapp.com/icons/{}/{}".format(dc_id,dc_icon)
                    created = at_obj.create("discord",{"id":dc_id,
                                                       "name":dc_name,
                                                       'thumb':[{'url':img_url}]})
                    dc_rid = created.get('id')
                    discord_map[dc_id] ={'rid':dc_rid,
                              'wallets':[]}
                else:
                    dc_rid = discord_map[dc_id]['rid']
                wallets = discord_map[dc_id]['wallets']
                if name not in wallets:
                    wallets.append(name)
                    at_obj.update("discord",dc_rid,{"wallets":wallets})
                    discord_map[dc_id]['wallets'].append(name)

def leave_dc_list():
    wallets_map = {}
    wallets = at_obj.get_all("emails").get('records')
    for wal in wallets:
        fields = wal.get('fields')
        name = fields.get("ID", '')
        dc_token = fields.get("discord token", '')
        wallets_map[name] = dc_token
    discords = at_obj.get_all("discord").get('records')
    for wal in discords:
        rid = wal.get('id')
        fields = wal.get('fields')
        dc_id = fields.get("id", '')
        name = fields.get("name", '')
        dc_wallets = fields.get("wallets", [])
        Status = fields.get("Status", "")
        if Status == "leave":
            for w in dc_wallets:
                print ("levaing {} {}".format(w,name))
                bot = discum.Client(token=wallets_map[w], log=False)
                bot.leaveGuild(dc_id)
            at_obj.delete("discord",rid)
update_dc_list()
#leave_dc_list()
