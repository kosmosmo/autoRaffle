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
    if not os.path.exists(root_path + 'alpha_cache.json'):
        data = {}
        _write_cache(data)
    f = open(root_path + 'alpha_cache.json')
    data = json.load(f)
    return data

def _write_cache(data):
    with open(root_path + "alpha_cache.json", "w") as outfile:
        json.dump(data, outfile, indent=4)

class alphaJobs_c(alphaJobs):
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


    def _pick_tw(self,tw_id):
        self.driver.execute_script("window.scrollTo(0, 2000)")
        tw_dropdown = self.driver.find_elements(By.CLASS_NAME,
                                                       'MuiSelect-select.MuiSelect-standard.MuiInput-input.MuiInputBase-input.css-1yzqhai')
        if not tw_dropdown:
            return
        try:
            tw_dropdown[-1].click()
            time.sleep(3)
            tw_options = self.driver.find_elements(By.CLASS_NAME,
                                                           'MuiMenuItem-root.MuiMenuItem-gutters.MuiButtonBase-root.css-10xh66c')
            correct_tw = tw_options[0]
            for tw in tw_options:
                if str(tw.text).strip().lower() == tw_id.lower():
                    correct_tw = tw
                    break
            time.sleep(5)
            correct_tw.click()
        except:
            pass

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
                #at_obj.delete("alpha list",self.rid)
                print ('raffl over!')
            except:
                pass
            self.driver.quit()
            return
        try:
            fields = at_obj.get("alpha list",self.rid).get('fields')
            status = fields.get('status','')
        except:
            status = ''
        while not status:
            time.sleep(120)
            try:
                status = at_obj.get("alpha list",self.rid).get('fields').get('status', '')
            except:
                status = ""
        try:
            reg_btn = self.driver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
            reg_btn.click()
            time.sleep(10)
        except:
            pass
        if not self._check_success_reg():
            find_rec = at_obj.get("alpha list", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                'records')
            if find_rec:
                rid = find_rec[0].get('id')
                cur_ct = find_rec[0].get('fields').get('fail count', 0)
                fail = find_rec[0].get('fields').get('fail reason', "")
                if not fail:
                    fail = "unknown"
                at_obj.update("alpha list", rid, {"fail count": cur_ct + 1,
                                                  "fail reason":fail})
        self.driver.quit()