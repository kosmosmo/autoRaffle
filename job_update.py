from airtable_wrapper import AirtableWrapper
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import twitter_job
import time
import random
import utils as u
import os
root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
tw_cache = u.get_twitter_cache()

def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
data = _get_key()
at_keys = data["at_keys"]
key = random.choice(at_keys)

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
        elif  url.startswith("https://twitter.com/") and  "tweet_id=" in url:
            parsed_url = urlparse(url)
            status = parse_qs(parsed_url.query)['tweet_id'][0]
            follow_links.add("https://twitter.com/user/status/" + status)
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

def clean_pref():
    pref_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    to_address = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\Preferences"
    import shutil
    shutil.copyfile(to_address, pref_file_path)

def delet_bad_pref():
    import os
    bad_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences.bad'
    pref_file_path =  r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    if os.path.exists(bad_file_path):
        os.remove(bad_file_path)
        print ("deleted bad pref!!")
        time.sleep(10)
    if os.path.exists(pref_file_path):
        try:
            clean_pref()
            print("clean pref!!")
        except:
            pass
        time.sleep(10)

def auto_clean_pref():
    import os
    bad_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences.bad'
    pref_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    if os.path.exists(bad_file_path) and os.path.getsize(bad_file_path) > 100000:
        os.remove(bad_file_path)
        print("deleted bad pref!!")
        time.sleep(5)
    if os.path.exists(pref_file_path)  and os.path.getsize(pref_file_path) > 100000:
        try:
            clean_pref()
            print("clean pref!!")
        except:
            pass
        time.sleep(5)


def run_jobs():
    i = 1
    rand_time = random.randint(1, 100)
    time.sleep(rand_time)
    cache = _get_cache()
    all_list = at_obj.get_all("raffle list").get('records')
    delet_bad_pref()

    for item in all_list:
        auto_clean_pref()
        flag = False
        j = 0
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
                if rid not in cache:
                    time.sleep(5)
                flag = True
                i += 1
            except:
                j += 1
                print ("retry.................." + str(j))
                import os
                os.system("taskkill /im chrome.exe /f")



import random
print ("START!!")
run_jobs()
print ("DONE")
