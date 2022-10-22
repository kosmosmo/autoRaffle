import undetected_chromedriver as webdriver
from airtable_wrapper import AirtableWrapper
#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException
#from selenium.webdriver import ActionChains
#from selenium.webdriver.common.keys import Keys
import time,random,json,os
#from urllib.parse import urlparse
#from urllib.parse import parse_qs
#from alpha_sel_profiles import profileJob
#import twitter_job
import random,pprint
from job_queue.job_queue import alpha_job, premint_job,job_queue


filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
root_path = os.path.dirname(os.path.realpath(__file__)) + '\\'
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
    if not os.path.exists(root_path + 'alpha_cache.json'):
        data = {}
        _write_cache(data)
    f = open(root_path + 'alpha_cache.json')
    data = json.load(f)
    return data
def _write_cache(data):
    with open(root_path + "alpha_cache.json", "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_alpha_job(res):
    job_list = at_obj.get_all("alpha list").get('records')
    cache = _get_cache()
    res = res
    for item in job_list:
        rid = item.get('id')
        fields = item.get('fields')
        url = fields.get('url')
        machines = fields.get('machine (from alpha index)')
        name = fields.get('Name (from alpha index)')[0]
        keyword = fields.get('keyword (from alpha index)')[0]
        time =  fields.get('time','')
        ignore = fields.get('ignore cache',False)
        if "All" in machines or machine_name in machines:
            if url not in cache or ignore:
                alpha_job_obj = alpha_job(time,url,keyword,rid)
                res.append(alpha_job_obj)
    return res

def get_premint_job(res):
    return res

while True:
    print ('starting........!')
    rand_time = random.randint(1, 100)
    time.sleep(rand_time)
    print ('#############################################################')
    alpha_jobs = get_alpha_job([])
    b = job_queue(alpha_jobs)
    b.sort()
    b.run()
    print('#############################################################')
    print ('done...! Sleep for 1000 sec!')
    time.sleep(1000)
