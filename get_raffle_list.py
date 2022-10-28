from airtable_wrapper import AirtableWrapper
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
import json
import time
from datetime import datetime, timedelta
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

options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, use_subprocess=True)

def get_raffle_requritement(url):

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
            if "?" in tweet_id:
                tweet_id = tweet_id.split("?")[0]
            retweet_links.add("https://twitter.com/intent/retweet?tweet_id="+tweet_id)
        elif url not in filter_out:#premint follow
            user = url.split("https://twitter.com/")[1]
            user = user.replace("@","")
            follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
    details = get_details(driver)
    print (details)
    return [remove_case_insenstive(list(retweet_links)),remove_case_insenstive(list(follow_links)),details]

def remove_case_insenstive(org_list):
    res = []
    marker = set()
    for item in org_list:
        item_low = item.lower()
        if item_low not in marker:
            marker.add(item_low)
            res.append(item)
    return res


def get_details(driver):
    res = {}
    other_fields = ["MINT PRICE", "TOTAL SUPPLY", "NUMBER OF WINNERS","VERIFIED TWITTER"]
    time_convert = ["REGISTRATION CLOSES","MINT DATE","RAFFLE TIME"]
    elms = driver.find_elements(By.CLASS_NAME, 'col-6.col-lg-4.mb-4')
    for item in elms:
        text = item.text
        vals = text.split('\n')
        if len(vals) >=2:
            key = vals[0]
            val = vals[1]
            if key in time_convert:
                print (key,val)
                dt_time = convert_to_datetime(val)
                at_time = convert_to_airtable_time(dt_time)
                res[key] = at_time
            elif key in other_fields:
                res[key] = val
    if 'VERIFIED TWITTER' in res and res['VERIFIED TWITTER']:
        res['VERIFIED TWITTER'] = "https://twitter.com/" + res['VERIFIED TWITTER'].split(" ")[0]
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
            update_content = {
                "status" : "Ready",
                "retweet_links":retweet_links,
                "follow_links":follow_links
            }
            update_content.update(links[2])
            at_obj.update("raffle list",rid,update_content)

def convert_to_datetime(str_time):
    str_time = str_time.lstrip("🚨")
    if "month" in str_time:
        h = 30 * 24
        return datetime.now() + timedelta(hours=h)
    if "week" in str_time:
        h = 7 * 24
        split = str_time.split(" week")
        if len(split) >= 1:
            h = 7*24*int(split[0])
        return datetime.now() + timedelta(hours=h)
    if "hours" in str_time or "minutes" in str_time:
        split = str_time.split(" hour")
        h = 0
        m = 0
        if len(split) >= 2:
            h = int(split[0])
        try:
            split2 = split[1].split(", ")
            if len(split2) >= 1:
                m = int(split2[1].split(" minute")[0])
            print (m)
        except:
            h=-24
        return datetime.now() + timedelta(hours=h, minutes=m)



    str_time =  str_time.replace("p.m.","PM")
    str_time = str_time.replace("a.m.", "AM")
    str_time = str_time.replace("noon", "12 PM")
    str_time = str_time.replace("midnight", "12 AM")
    if str_time.endswith("UTC"):
        str_time = str_time.split(" UTC")[0]
        dt = strptime_tries(str_time)
        dt = dt - timedelta(hours=4)
        return dt
    dt = strptime_tries(str_time)
    return dt

def strptime_tries(str_time):
    try:
        dt = datetime.strptime(str_time, "%b. %d, %Y %I %p")
        return dt
    except:
        pass
    try:
        dt = datetime.strptime(str_time, "%b. %d, %Y, %I:%M %p")
        return dt
    except:
        pass
    try:
        dt = datetime.strptime(str_time, "%b. %d, %Y, %I %p")
        return dt
    except:
        pass
    try:
        dt = datetime.strptime(str_time, "%b. %d, %Y")
        return dt
    except:
        pass
    try:
        dt = datetime.strptime(str_time, "%b. %d, %Y %I:%M %p")
        return dt
    except:
        pass



def convert_to_airtable_time(date_time):
    at_time =  date_time.strftime("%Y-%m-%dT%H:%M:%S"+".000Z")
    return at_time


def _get_cache():
    f = open(root_path + 'cache.json')
    data = json.load(f)
    return data

def _write_cache(data):
    with open(root_path + "cache.json", "w") as outfile:
        json.dump(data, outfile, indent=4)
#get_links()