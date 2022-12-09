import json,os
from airtable_wrapper import AirtableWrapper
root_path =  os.path.dirname(os.path.realpath(__file__)) + '\\'
import requests

def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data['key']
key = _get_key()
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)

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
        _write_cache("tw_cache.json", data)
    else:
        data = _get_cache("tw_cache.json")
    return data

def get_id(url):
    if "screen_name=" in url:
        return url.split("screen_name=")[-1].lower()
    if "tweet_id=" in url:
        return url.split("tweet_id=")[-1].lower()
    if "/status/" in url:
        return url.split("/status/")[-1].lower()
    if "https://twitter.com/" in url:
        return url.split("https://twitter.com/")[-1].lower()

def get_black_list(all_list):
    res = set()
    for item in all_list:
        fields = item.get('fields')
        rid = item.get('id')
        name = fields.get("Name")
        res.add(name.lower())
    return res

def get_white_list(all_list):
    res = set()
    for item in all_list:
        fields = item.get('fields')
        rid = item.get('id')
        name = fields.get("Name")
        res.add(name.lower())
    return res

class twitter_scan():
    def __init__(self,bearer_token):
        self.bearer_token = bearer_token

    def _get_user_data_url(self,user_name):
        usernames = "usernames=" + user_name
        user_fields = "user.fields=description,created_at"
        url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
        return url

    def _get_following_url(self,user_id): #singular
        return "https://api.twitter.com/2/users/{}/following".format(user_id)

    def get_user_id(self,user_name):
        url = self._get_user_data_url(user_name)
        return self.connect_to_endpoint(url).get("data",[{}])[0].get("id","")

    def get_name(self,user_name):
        url = self._get_user_data_url(user_name)
        return self.connect_to_endpoint(url).get("data",[{}])[0].get("name","")

    def get_recent_follow(self,user_id):
        url = self._get_following_url(user_id)
        params = {"user.fields": "created_at"}
        data = self.connect_to_endpoint(url,params=params).get("data",{})
        return data

    def convert_to_cache(self,data):
        res = {}
        for item in data:
            res[item.get("username")] = item
        return res

    def _write_cache(self,data,path):
        with open(path, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def _get_cache(self,path):
        f = open(path)
        data = json.load(f)
        return data

    def bearer_oauth(self,r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "v2UserLookupPython"
        return r


    def connect_to_endpoint(self,url,params=""):
        response = requests.request("GET", url, auth=self.bearer_oauth, params=params)
        if response.status_code != 200:
            print( Exception(str(response.status_code) + " " +
                "Request returned an error: {} {}".format(
                    response.status_code, response.text
                )
            ))
            return {}
        return response.json()
