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

class alphaJobs_c_local(alphaJobs):
    def __init__(self, url, keyword, rid):
        alphaJobs.__init__(self, url, keyword, rid)
        self.url = url
        self.keyword= keyword
        self.rid = rid


    def on_start(self):
        self.driver = self.get_driver()
        time.sleep(2)
        self.driver.maximize_window()
        time.sleep(2)
        loaded = False
        while not loaded:
            try:
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'MuiPaper-root')))
                loaded = True
            except Exception as e:
                self.driver.refresh()
                time.sleep(5)
                if len(self.driver.window_handles) >=3:
                    loaded = True
        time.sleep(5)


    def get_driver(self,profile="Default"):
        options = webdriver.ChromeOptions()
        options.add_argument(self.url)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory='+profile)
        return webdriver.Chrome(options=options,use_subprocess=True)


    def run(self):
        self.on_start()
        while len(self.driver.window_handles) >=3:
            time.sleep(5)
            self.driver.quit()
            time.sleep(5)
            self.on_start()

        self._click_reg()
        self.driver.quit()
        #if profiles:
        #    for item in profiles:
        #        auto_clean_pref(item,"pref\\"+item)
        #    p = profileJob(self.url,profiles)
        #    p.run()


    def _click_reg(self):
        if self._check_captcha():
            find_rec = at_obj.get("alpha list", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                'records')
            if find_rec:
                rid = find_rec[0].get('id')
                fail = find_rec[0].get('fields').get('fail reason', "")
                if not fail or fail == "unknow":
                    at_obj.update("alpha list", rid, {"fail reason": "captcha"})
            self.driver.quit()
            return
        if not self._check_over():
            try:
                at_obj.delete("alpha list",self.rid)
                print ('raffl over!')
            except:
                pass
            self.driver.quit()
            return
        print ("ready")
        req = self.get_raffle_requritement()
        self.driver.quit()
        tw_job = twitter_job.twitterJobs(req[0], req[1], check_cache=False)
        tw_job.run()
        time.sleep(1)
        tw_undo_list = _get_cache()
        for item in req[0]:
            tw_undo_list["retweet"] = item
        for item in req[1]:
            tw_undo_list["follow"] = item
        _write_cache(tw_undo_list)
        at_obj.update("alpha list",self.rid,{"status":"ready"})

import job_queue
from job_queue import base_job

class alpha_job_c(base_job):
    def __init__(self,close_time,url,keyword,rid):
        base_job.__init__(self,close_time)
        self.type = "alpha"
        self.rid = rid
        self.twitter_job = alphaJobs_c_local(url,keyword,rid)
        if not self.close_time:
            self.close_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            self.close_time = job_queue.convert_to_airtable_time(self.close_time)
        else:
            self.close_time = self.close_time.replace('T',' ')[:-5]

    def __repr__(self):
        return self.close_time + " " + self.type + " " + self.rid

    def run(self):
        self.twitter_job.run()

def get_alpha_job():
    job_list = at_obj.get_all("alpha list").get('records')
    res = []
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
        status = fields.get('status',"")
        if skip:
            continue

        if status:
            continue
        alpha_job_obj = alpha_job_c(time, url, keyword, rid)
        if machine_name in machines or  "All" in machines:
            res.append(alpha_job_obj)
    return res



a = get_alpha_job()
a_sorted = sorted(a,key=lambda x:x.close_time)
for item in a_sorted:
    print (item)
    item.run()
