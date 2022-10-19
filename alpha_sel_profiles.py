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
import random

root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
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

class profileJob():
    def __init__(self, url, profiles):
        self.url = url
        self.profiles = profiles

    def get_driver(self,profile="Default"):
        options = webdriver.ChromeOptions()
        options.add_argument(self.url)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory='+profile)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def run(self):
        for item in self.profiles:
            profile_dirver = self.get_driver(item)
            profile_dirver.maximize_window()
            time.sleep(2)
            loaded = False
            while not loaded:
                try:
                    WebDriverWait(profile_dirver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'MuiPaper-root')))
                    loaded = True
                except:
                    time.sleep(5)
            time.sleep(5)
            self._reg(profile_dirver)


    def _reg(self,profile_dirver):
        try:
            reg_btn = profile_dirver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
        except:
            profile_dirver.quit()
            return
        time.sleep(2)
        reg_btn.click()
        time.sleep(12)
        profile_dirver.quit()