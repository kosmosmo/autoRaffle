from airtable_wrapper import AirtableWrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,random,json,os
from urllib.parse import urlparse
from urllib.parse import parse_qs
from alpha_sel_profiles import profileJob
import twitter_job
import random

filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
root_path =  os.path.dirname(os.path.realpath(__file__)) + '\\'
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
data = _get_key()
at_keys = data["at_keys"]
key = random.choice(at_keys)
machine_name = data.get('name','All')
profiles = data.get("profile",[])
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)

p_list = at_obj.get_all("projects").get('records')
for item in p_list:
    rid = item.get('id')
    fields = item.get('fields')
    twitter = fields.get('twitter')
    if not twitter:
        continue
    if twitter and not twitter.startswith('https://twitter.com/'):
        print (twitter)
        continue
    if "user?screen_name=" in twitter:
        twitter = "https://twitter.com/" + twitter.split("user?screen_name=")[-1]
    if "?" in twitter:
        twitter = twitter.split('?')[0]
    if twitter.endswith('/'):
        twitter = twitter[:-1]
    at_obj.update("projects",rid,{"twitter":twitter})
