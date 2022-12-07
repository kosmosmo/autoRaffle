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
def _get_cache(cache_file):
    import os
    if not os.path.exists(root_path + cache_file):
        data = {}
        _write_cache(data,cache_file)
    f = open(root_path + cache_file)
    data = json.load(f)
    return data

def _write_cache(data,cache_file):
    with open(root_path + cache_file, "w") as outfile:
        json.dump(data, outfile, indent=4)


def get_alpha_job_shard(res):
    job_list = at_obj.get_all("alpha list").get('records')
    cache = _get_cache('alpha_cache.json')
    res = res
    twitter_machine_jobs = []
    for item in job_list:
        rid = item.get('id')
        fields = item.get('fields')
        url = fields.get('url')
        machines = fields.get('machine (from alpha index)')
        name = fields.get('Name (from alpha index)')[0]
        keyword = fields.get('keyword (from alpha index)')[0]
        time =  fields.get('time','')
        ignore = fields.get('ignore cache',False)
        skip =  fields.get('skip',False)
        assigned_machine = fields.get('assigned machine',[""])[0]
        if skip:
            continue
        if url in cache and not ignore:
            continue
        if not assigned_machine or not assigned_machine[0]:
            continue

        alpha_job_obj = alpha_job(time, url, keyword, rid)
        if assigned_machine == machine_name:
            twitter_machine_jobs.append(alpha_job_obj)
        else:
            if machine_name in machines or  "All" in machines:
                res.append(alpha_job_obj)
    return [res,twitter_machine_jobs]

def get_alpha_job(res):
    job_list = at_obj.get_all("alpha list").get('records')
    cache = _get_cache('alpha_cache.json')
    res = res
    twitter_machine_jobs = []
    for item in job_list:
        rid = item.get('id')
        fields = item.get('fields')
        url = fields.get('url')
        machines = fields.get('machine (from alpha index)')
        name = fields.get('Name (from alpha index)')[0]
        keyword = fields.get('keyword (from alpha index)')[0]
        time =  fields.get('time','')
        ignore = fields.get('ignore cache',False)
        skip =  fields.get('skip',False)
        if skip:
            continue
        if url in cache and not ignore:
            continue

        alpha_job_obj = alpha_job(time, url, keyword, rid)
        if machine_name in machines or  "All" in machines:
            res.append(alpha_job_obj)
    return [res,[]]


def get_premint_job(res):
    all_list = at_obj.get_all("raffle list").get('records')
    cache = _get_cache('cache.json')
    res = res
    for item in all_list:
        fields = item.get('fields')
        status = fields.get('status', None)
        rid = item.get('id')
        time = fields.get('REGISTRATION CLOSES','')
        if status == "Ready" and rid not in cache:
            retweet_links = fields.get('retweet_links')
            if retweet_links:
                retweet_links = retweet_links.split('\n')
            else:
                retweet_links = []
            follow_links = fields.get('follow_links')
            if follow_links:
                follow_links = follow_links.split('\n')
            else:
                follow_links = []
            premint_job_obj = premint_job(time,rid,retweet_links,follow_links)
            res.append(premint_job_obj)
    return res

while True:
    try:
        print ('starting........!')

        rand_time = random.randint(1,120)
        #if machine_name in ["watergua","pink","lemon","lychee","pear","grape","pineapple"]:  ####using shard mode
        #    rand_time = 2                                                                    ####using shard mode
        time.sleep(rand_time)
        print ('#############################################################')
        #alpha_jobs_all = get_alpha_job_shard([])                            ####using shard mode
        #twitter_machine_jobs = alpha_jobs_all[1]                            ####using shard mode
        alpha_jobs_all  = get_alpha_job([])                                  #using regular mode
        twitter_machine_jobs = []                                            #using regular mode
        raffle_machine_jobs = alpha_jobs_all[0]
        print (twitter_machine_jobs,raffle_machine_jobs)
        all_jobs = get_premint_job(raffle_machine_jobs)
        b = job_queue(all_jobs,twitter_machine_jobs=twitter_machine_jobs)
        b.sort()
        #b.sort_shard()                ####using shard mode
        b.run()
        print('#############################################################')
        print ('done...! Sleep for 500 sec!')
        time.sleep(500)
    except Exception as e:
        print (e)
        for i in range(10):
            print (".................................")
        time.sleep(60)


