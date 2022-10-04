from airtable_wrapper import AirtableWrapper
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import twitter_job
import time
root_path = "C:\\Users\\kosmo\\PycharmProjects\\autoRaffle\\"
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data['key']
key = _get_key()

at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)
filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]



def get_raffle_requritement(url):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options, use_subprocess=True)
    print (url)
    driver.get(url)
    retweet_links = set()
    follow_links = set()
    elems = driver.find_elements(by=By.XPATH, value="//a[@href]")
    for elem in elems:
        url = elem.get_attribute("href")
        if not url.startswith("https://twitter.com/"):
            continue
        if  "screen_name=" in url:#alpha follow
            parsed_url = urlparse(url)
            user = parse_qs(parsed_url.query)['screen_name'][0]
            follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
        elif "tweet_id=" in url:#alpha retweet
            retweet_links.add(url)
        elif "/status/" in url: #premint retweet
            tweet_id = url.split("/status/")[1]
            retweet_links.add("https://twitter.com/intent/retweet?tweet_id="+tweet_id)
        elif url not in filter_out:#premint follow
            user = url.split("https://twitter.com/")[1]
            follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
    return [remove_case_insenstive(list(retweet_links)),remove_case_insenstive(list(follow_links))]

def remove_case_insenstive(org_list):
    res = []
    marker = set()
    for item in org_list:
        item_low = item.lower()
        if item_low not in marker:
            marker.add(item_low)
            res.append(item)
    return res




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
get_links()