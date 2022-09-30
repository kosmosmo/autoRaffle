from airtable_wrapper import AirtableWrapper
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import twitter_job
import time
root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data['key']
key = _get_key()

at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)
filter_out = [
    "https://twitter.com/premint_nft"
]



def get_raffle_requritement(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options, use_subprocess=True)
    driver.get(url)
    retweet_links = set()
    follow_links = set()
    elems = driver.find_elements(by=By.XPATH, value="//a[@href]")
    for elem in elems:
        url = elem.get_attribute("href")
        print(url)
        if url.startswith("https://twitter.com/") and "screen_name=" in url:
            parsed_url = urlparse(url)
            user = parse_qs(parsed_url.query)['screen_name'][0]
            follow_links.add("https://twitter.com/" + user)
        elif url.startswith("https://twitter.com/") and "status" in url:
            retweet_links.add(url)
        elif url.startswith("https://twitter.com/") and url not in filter_out:
            follow_links.add(url)
    return [list(retweet_links),list(follow_links)]

def get_links():
    all_list = at_obj.get_all("raffle list").get('records')
    for item in all_list:
        fields = item.get('fields')
        status = fields.get('status',None)
        rid = item.get('id')
        if not status:
            url = fields.get('url')
            links = get_raffle_requritement(url)
            retweet_links = "\n".join(links[0])
            follow_links = "\n".join(links[1])
            at_obj.update("raffle list",rid,{
                "status" : "Ready",
                "retweet_links":retweet_links,
                "follow_links":follow_links
            })




def _get_cache():
    f = open(root_path + 'cache.json')
    data = json.load(f)
    return data

def _write_cache(data):
    with open(root_path + "cache.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

def run_jobs():
    i = 1
    cache = _get_cache()
    all_list = at_obj.get_all("raffle list").get('records')
    for item in all_list:
        j = 0
        flag = False
        while j < 3 and not flag:
            try:
                print ("starting job Number " + str(i) + " ........................")
                fields = item.get('fields')
                status = fields.get('status',None)
                rid = item.get('id')
                if status == "Ready" and rid not in cache:
                    retweet_links = fields.get('retweet_links')
                    if retweet_links:
                        retweet_links = retweet_links.split('\n')
                    else:
                        retweet_links = []
                    follow_links =  fields.get('follow_links')
                    if follow_links:
                        follow_links = follow_links.split('\n')
                    else:
                        follow_links = []
                    tw_job = twitter_job.twitterJobs(retweet_links,follow_links)
                    tw_job.run()
                    cache[rid] = ''
                    _write_cache(cache)
                i += 1
                if rid not in cache:
                    time.sleep(5)
                flag = True
            except:
                j += 1


import urllib.request
import zipfile
zip = "https://github.com/kosmosmo/autoRaffle/archive/refs/heads/master.zip"
dir = r"C:\Users\Administrator\Desktop\bot.zip"
base_dir = r"C:\Users\Administrator\Desktop"
urllib.request.urlretrieve(zip, dir)
with zipfile.ZipFile(dir, 'r') as zip_ref:
    zip_ref.extractall(base_dir)
import random
print ("START!!")
rand_time = random.randint(1,100)
time.sleep(rand_time)
run_jobs()
