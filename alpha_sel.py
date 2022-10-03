import undetected_chromedriver as webdriver
from airtable_wrapper import AirtableWrapper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,random,json
from urllib.parse import urlparse
from urllib.parse import parse_qs
import twitter_job

filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]
root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
data = _get_key()
key = data['key']
machine_name = data.get('name','All')

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

class alphaJobs():
    def __init__(self,url,keyword,rid):
        self.url = url
        self.keyword= keyword
        self.rid = rid
        self.driver = self.get_driver()
        time.sleep(3)
        self.driver.maximize_window()
        time.sleep(3)

    def get_driver(self):
        options = webdriver.ChromeOptions()
        time.sleep(2)
        options.add_argument(self.url)
        time.sleep(2)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        time.sleep(2)
        options.add_argument(r'--profile-directory=Default')
        time.sleep(2)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def run(self):
        self._click_reg()
        self.driver.quit()

    def get_raffle_requritement(self,url):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options, use_subprocess=True)
        driver.get(url)
        retweet_links = set()
        follow_links = set()
        elems = driver.find_elements(by=By.XPATH, value="//a[@href]")
        for elem in elems:
            url = elem.get_attribute("href")
            if not url.startswith("https://twitter.com/"):
                continue
            if "screen_name=" in url:  # alpha follow
                parsed_url = urlparse(url)
                user = parse_qs(parsed_url.query)['screen_name'][0]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
            elif "tweet_id=" in url:  # alpha retweet
                retweet_links.add(url)
            elif "/status/" in url:  # premint retweet
                tweet_id = url.split("/status/")[1]
                retweet_links.add("https://twitter.com/intent/retweet?tweet_id=" + tweet_id)
            elif url not in filter_out:  # premint follow
                user = url.split("https://twitter.com/")[1]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
        return [list(retweet_links), list(follow_links)]

    def _check_over(self):
        try:
            over = self.driver.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-h5')
            if "You're not a winner. Maybe next time!" in over.text or "You're a winner! Congratulations" in over.text or "Raffle is over." in over.text:
                return False
            return True
        except:
            return True


    def _find_error(self):
        errors = self.driver.find_elements(By.CLASS_NAME, 'MuiAlert-standardError')
        for item in errors:
            if "join" in item.text.lower() and "discord" in item.text.lower() and self.keyword.lower() not in item.text.lower():
                find_rec = at_obj.get("alpha fails", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                    'records')
                if not find_rec:
                    at_obj.create("alpha fails",{
                        "Url":self.url,
                        "Notes":item.text
                    })
                return False
        return True

    def _check_success_reg(self):
        time.sleep(7)
        try:
            checking = self.driver.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-h5.css-1l3cl22')
        except:
            return False
        if checking:
            return True
        return False

    def _get_raffle_requritement(self):
        retweet_links = set()
        follow_links = set()
        elems = self.driver.find_elements(by=By.XPATH, value="//a[@href]")
        for elem in elems:
            url = elem.get_attribute("href")
            if not url.startswith("https://twitter.com/"):
                continue
            if "screen_name=" in url:  # alpha follow
                parsed_url = urlparse(url)
                user = parse_qs(parsed_url.query)['screen_name'][0]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
            elif "tweet_id=" in url:  # alpha retweet
                retweet_links.add(url)
            elif "/status/" in url:  # premint retweet
                tweet_id = url.split("/status/")[1]
                retweet_links.add("https://twitter.com/intent/retweet?tweet_id=" + tweet_id)
            elif url not in filter_out:  # premint follow
                user = url.split("https://twitter.com/")[1]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
        return [list(retweet_links), list(follow_links)]

    def _click_reg(self):
        if not self._check_over():
            try:
                at_obj.delete("alpha list",self.rid)
                print ('raffl over!')
            except:
                pass
            self.driver.quit()
            return
        try:
            reg_btn = self.driver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
        except:
            return
        time.sleep(7)
        reg_btn.click()
        time.sleep(12)
        checker = self._find_error()
        if checker:
            if self._check_success_reg():
                self.driver.quit()
                return
            req = self._get_raffle_requritement()
            self.driver.quit()
            tw_job = twitter_job.twitterJobs(req[0], req[1])
            tw_job.run()
            time.sleep(5)
            self.driver = self.get_driver()
            time.sleep(10)
            try:
                reg_btn_new = self.driver.find_element(By.CSS_SELECTOR,
                                                   '.MuiButton-root[data-action ="view-project-register"]')
                reg_btn_new.click()
            except:
                pass
        if not self._check_success_reg():
            find_rec = at_obj.get("alpha fails", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                'records')
            if not find_rec:
                at_obj.create("alpha fails", {
                    "Url": self.url,
                    "Notes": "unknown"
                })
        self.driver.quit()

def run_all_jobs():
    job_list = at_obj.get_all("alpha list").get('records')
    cache = _get_cache()
    i = 1
    for item in job_list:
        rid = item.get('id')
        fields = item.get('fields')
        url = fields.get('url')
        machines = fields.get('machine (from alpha index)')
        name = fields.get('Name (from alpha index)')[0]
        keyword = fields.get('keyword (from alpha index)')[0]
        if "All" in machines or machine_name in machines:
            print("ALPHA job ............" + str(i) + '........' + name)
            tried = 0
            while tried < 3:
                try:
                    if url not in cache:
                        job = alphaJobs(url,keyword,rid)
                        job.run()
                        cache[url] = ""
                        _write_cache(cache)
                        time.sleep(10)
                    tried = 4
                except:
                    tried += 1
            i += 1
        else:
            print ('skip ' + name)

def delet_bad_pref():
    import os
    bad_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences.bad'
    pref_file_path =  r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    if os.path.exists(bad_file_path):
        os.remove(bad_file_path)
        print ("deleted bad pref!!")
        time.sleep(5)
    if os.path.exists(pref_file_path):
        os.remove(pref_file_path)
        print ("deleted bad pref!!")
        time.sleep(5)

delet_bad_pref()
run_all_jobs()
