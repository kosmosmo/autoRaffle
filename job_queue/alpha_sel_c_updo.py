import time,random,json,os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import undetected_chromedriver as webdriver
from airtable_wrapper import AirtableWrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from alpha_sel_q import alphaJobs
from urllib.parse import urlparse
from urllib.parse import parse_qs
from alpha_sel_profiles import profileJob
import twitter_job,os
import random
import pprint
import datetime
filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
root_path =os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+ '\\'
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

def _get_cache():
    import os
    if not os.path.exists(root_path + '/job_queue/tw_undo_list.json'):
        data = {}
        _write_cache(data)
    f = open(root_path + '/job_queue/tw_undo_list.json')
    data = json.load(f)
    return data

def _write_cache(data):
    with open(root_path + "/job_queue/tw_undo_list.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

data = _get_cache()
retweet_data = data["retweet"]
retweets = []
for key,val in retweet_data.items():
    retweets.append(key)

follow_data = data["follow"]
follows = []
for key,val in follow_data.items():
    follows.append(key)

total = len(follows) + len(retweets)
tw_job = twitter_job.twitterJobs_undo(retweets, follows,total = total)
tw_job.run()
data = {
    "retweet":{},
    "follow":{}
}
_write_cache(data)