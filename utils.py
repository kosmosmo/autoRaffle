import json,os
root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
default_data = {
            "follow":{},
            "retweet":{}
        }

def _get_cache(cache_file):
    f = open(root_path + cache_file)
    data = json.load(f)
    return data

def _write_cache(cache_file,data):
    with open(root_path + cache_file, "w") as outfile:
        json.dump(data, outfile, indent=4)

def get_twitter_cache():
    tw_cahce = root_path + "tw_cache.json"
    if not os.path.exists(tw_cahce):
        data = default_data
    else:
        data = _get_cache("tw_cache.json")
    return data

def get_id(url):
    if "screen_name=" in url:
        return url.split("screen_name=")[-1]
    if "tweet_id=" in url:
        return url.split("tweet_id=")[-1]
    if "/status/" in url:
        return url.split("/status/")[-1]
    if "https://twitter.com/" in url:
        return url.split("https://twitter.com/")[-1]
