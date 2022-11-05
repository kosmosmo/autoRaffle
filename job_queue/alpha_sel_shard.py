import time,random,json,os,sys
#sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import undetected_chromedriver as webdriver
from airtable_wrapper import AirtableWrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from urllib.parse import urlparse
from urllib.parse import parse_qs
from alpha_sel_profiles import profileJob
import twitter_job,os
import random
import alpha_sel_q as alpha_q
import pprint

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





class alphaJobs_shard(alpha_q.alphaJobs):
    def __init__(self,url,keyword,rid):
        alpha_q.alphaJobs.__init__(self,url,keyword,rid)
        self.twitter_machine = at_obj.get("alpha list",self.rid).get("fields").get("assigned machine",[""])[0]
        self.twitter_machine_id = self.get_twitter_machine_id()



    def get_twitter_machine_id(self):
        tw_all = at_obj.get_all("twitter").get('records')
        for item in tw_all:
            fields = item.get('fields')
            machine = fields.get('machine')
            twitter_id = fields.get('twitter id')
            if self.twitter_machine == machine:
                return twitter_id

    def _check_black_list(self):
        pass

    def _pick_tw(self):
        self.driver.execute_script("window.scrollTo(0, 2000)")
        tw_dropdown = self.driver.find_elements(By.CLASS_NAME,
                                                       'MuiSelect-select.MuiSelect-standard.MuiInput-input.MuiInputBase-input.css-1yzqhai')
        if not tw_dropdown:
            return
        tw_dropdown[2].click()
        time.sleep(3)
        tw_options = self.driver.find_elements(By.CLASS_NAME,
                                                       'MuiMenuItem-root.MuiMenuItem-gutters.MuiButtonBase-root.css-10xh66c')
        for tw in tw_options:
            if str(tw.text).strip().lower() == str(self.twitter_machine_id).strip().lower():
                tw.click()
                break


    def _reg_check(self):
        if self.twitter_machine == machine_name:
            print ("start twitter machine....")
            self._twitter_machine()
            return True
        retries = 0
        while retries < 3:
            status = at_obj.get("alpha list", self.rid).get("fields").get("status","")
            if status != "ready":
                time.sleep(200)
                retries += 1
            else:
                self._raffle_machine()
                return True
        return False

    def _twitter_machine(self):
        #check register error
        checker = self._find_error()
        if checker:
            if self._check_success_reg():
                self.driver.quit()
                return
            req = self.get_raffle_requritement()
            self.driver.quit()
            tw_job = twitter_job.twitterJobs(req[0], req[1])
            tw_job.run()
            time.sleep(2)
            ###########################################
            self.driver = self.get_driver()
            time.sleep(2)
            loaded = False
            while not loaded:
                try:
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'MuiPaper-root')))
                    loaded = True
                except:
                    self.driver.refresh()
                    time.sleep(5)
                    if len(self.driver.window_handles) >= 3:
                        loaded = True
            ###########################################
            time.sleep(7)
            at_obj.update("alpha list",self.rid,{"status":"ready"})
            try:
                self._pick_tw()
                reg_btn_new = self.driver.find_element(By.CSS_SELECTOR,
                                                   '.MuiButton-root[data-action ="view-project-register"]')
                reg_btn_new.click()
                time.sleep(12)
            except:
                pass

    def _raffle_machine(self):
        checker = self._find_error()
        if checker:
            try:
                self._pick_tw()
                reg_btn_new = self.driver.find_element(By.CSS_SELECTOR,
                                                       '.MuiButton-root[data-action ="view-project-register"]')
                reg_btn_new.click()
                time.sleep(12)
            except:
                pass

    def _update_register_status(self):
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



    def _update_job_status(self):
        if machine_name == self.twitter_machine:
            print ("status")
            at_obj.update("alpha list",self.rid,{"status":"ready"})

    def _click_reg(self):
        #skip raffle with captcha
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
        #skip ended raffle
        if not self._check_over():
            try:
                at_obj.delete("alpha list",self.rid)
                print ('raffl over!')
            except:
                pass
            self.driver.quit()
            return
        #find register button
        self._pick_tw()
        try:
            reg_btn = self.driver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
            time.sleep(2)
            reg_btn.click()
        except:
            pass

        if not self._check_success_reg():
            self._reg_check()
        time.sleep(12)
        self._update_register_status()
        self._update_job_status()
        self.driver.quit()

