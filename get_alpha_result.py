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
def _get_keys():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
keys = _get_keys()
bearer_token = keys["bearer_token"]
at_key = keys['key']
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",at_key)
CLIENT_FILE = "credentials.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]
service = google_apis.create_service(CLIENT_FILE,API_NAME,API_VERSION,SCOPES)
query_string = "is:unread Alphabot - You won"
save_location = os.getcwd()
root_path = "C:\\Users\\kosmo\\PycharmProjects\\autoRaffle\\"


class GmailException(Exception):
    """gmail base exception class"""


class NoEmailFound(GmailException):
    """no email found"""

def search_emails(query_stirng: str, label_ids: List = None):
    try:
        message_list_response = service.users().messages().list(
            userId='me',
            q=query_string
        ).execute()
        message_items = message_list_response.get('messages')
        next_page_token = message_list_response.get('nextPageToken')

        while next_page_token:
            message_list_response = service.users().messages().list(
                userId='me',
                q=query_string,
                pageToken=next_page_token
            ).execute()

            message_items.extend(message_list_response.get('messages'))
            next_page_token = message_list_response.get('nextPageToken')
        return message_items
    except Exception as e:
        raise NoEmailFound('No emails returned')

def get_message_detail(message_id, msg_format='metadata', metadata_headers: List = None):
    message_detail = service.users().messages().get(
        userId='me',
        id=message_id,
        format=msg_format,
        metadataHeaders=metadata_headers
    ).execute()
    return message_detail

def _get_emails(email):
    email_link = at_obj.search("emails", "email", email,id=True)
    if email_link:
        return [email_link.get('id')]
    return None

def get_emails():
    email_messages = search_emails(query_string)
    if not email_messages:
        return
    res = []

    for email_message in email_messages:
        messageDetail = get_message_detail(email_message['id'], msg_format='full', metadata_headers=['parts'])
        messageBody = messageDetail.get('payload', {}).get('parts',[{}])[0].get('body',{}).get('data')
        if not messageBody:
            messageBody =  messageDetail.get('payload', {}).get('body',{}).get('data')
        b = messageBody
        body = str(base64.urlsafe_b64decode(b))
        soup = BeautifulSoup(body, 'html.parser')
        soup_text = soup.get_text(separator="\n").split('\n')
        alpha_url = None
        machine = None
        for i in range(len(soup_text)):
            if soup_text[i].startswith('https://www.alphabot.app'):
                alpha_url = soup_text[i]
            elif soup_text[i].startswith('Anti-phishing code'):
                machine = soup_text[i+1]
        if not alpha_url:
            continue
        print (alpha_url,machine)
        tw_url_cache_path = '\cache\\tw_url_cache.json'
        tw_url_cache = _u._get_cache(tw_url_cache_path)
        if alpha_url not in tw_url_cache:
            tw_url = get_twitter_from_alpha(alpha_url)
            tw_name = get_twitter_name(tw_url)
            created_data = at_obj.create("projects",{
                "twitter":tw_url,
                "Name":tw_name,
                "wallet":"scanner"
            })
            rid = created_data.get('id')
            tw_url_cache[alpha_url] = rid
            _u._write_cache(tw_url_cache_path,tw_url_cache)
        else:
            rid = tw_url_cache[alpha_url]
        wallets = at_obj.get("projects",rid).get("fields").get('wallets',[])
        wallets.append(machine)
        at_obj.update("projects",rid,{"wallets":wallets})
        msg_id = email_message.get('id')
        service.users().messages().modify(userId='me', id=msg_id, body={'removeLabelIds': ['UNREAD']}).execute()
        time.sleep(1)
    return res

def get_twitter_from_alpha(url):
    try:
        scraper = cloudscraper.create_scraper(delay=10, browser={'custom': 'ScraperBot/1.0', })
        req = scraper.get(url)
        soup = BeautifulSoup(req.content, 'lxml')
        data = json.loads(soup.find('script', id='__NEXT_DATA__').text)
        tw_url = data.get('props').get('pageProps').get('project').get('twitterUrl')
        return tw_url
    except:
        return None

def get_twitter_name(tw_url):
    tw_obj = _u.twitter_scan(bearer_token)
    user_name = tw_url.split('/')[-1]
    return tw_obj.get_name(user_name)
get_emails()