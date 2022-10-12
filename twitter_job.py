import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,random
from urllib.parse import urlparse
from urllib.parse import parse_qs
import utils as u
import json,os
from airtable_wrapper import AirtableWrapper
tw_cache = u.get_twitter_cache()
root_path = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\"
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data['key']
key = _get_key()
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)

class twitterJobs():
    def __init__(self,retweet_links,follow_links):
        self.driver = self.get_driver()
        time.sleep(3)
        self.driver.maximize_window()
        time.sleep(3)
        self.driver.get("https://www.google.com/")
        time.sleep(3)
        self.retweet_links = retweet_links
        self.follow_links = follow_links
        all_list = at_obj.get_all("black_list").get('records')
        self.black_list = u.get_black_list(all_list)

    def get_driver(self):
        options = webdriver.ChromeOptions()
        time.sleep(2)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        time.sleep(2)
        options.add_argument(r'--profile-directory=Default')
        time.sleep(2)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def _check_status(self,status,url):
        time.sleep(8)
        try:
            if status == "followed":
                user = self._get_user_name(url)
                checking = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[aria-label ="Following @{}"]'.format(user))
                if checking:
                    tw_cache["follow"][u.get_id(url).lower()] = ""
                    u._write_cache("tw_cache.json",tw_cache)
            else:
                checking = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[data-testid ="{}"]'.format(status))
                if checking:
                    tw_cache["retweet"][u.get_id(url).lower()] = ""
                    u._write_cache("tw_cache.json", tw_cache)
            if checking:
                return True
            return False
        except:
            return False

    def run(self):
        time.sleep(2)
        for item in self.follow_links:
            if u.get_id(item) in self.black_list:
                continue
            if u.get_id(item) in tw_cache["follow"]:
                continue
            self.actions(item, "followed")
        for item in self.retweet_links:
            if u.get_id(item) in self.black_list:
                continue
            if u.get_id(item) in tw_cache["retweet"]:
                continue
            self.actions(item,"unretweet")
            self.actions(self._convert_like_url(item), "unlike")
        self.driver.quit()

    def _convert_like_url(self,url):
        return url.replace("intent/retweet","intent/like")

    def _get_user_name(self,url):
        parsed_url = urlparse(url)
        duser = parse_qs(parsed_url.query)['screen_name'][0]
        elems = self.driver.find_elements(by=By.XPATH, value="//a[@href]")
        for elem in elems:
            url = elem.get_attribute("href")
            photo_url = "https://twitter.com/" + duser + "/photo"
            nft_url  = "https://twitter.com/" + duser + "/nft"
            if url.lower() == photo_url.lower():
                return url.replace("https://twitter.com/",'').replace("/photo",'')
            if url.lower() == nft_url.lower():
                return url.replace("https://twitter.com/",'').replace("/nft",'')
        return duser

    def actions(self,url,status):
        #status "unretweet" for retweet
        #status "unlike" for like
        #status "followed" for follow
        flag = True
        while flag:
            self.driver.get(url)
            time.sleep(3)
            main = self.driver.window_handles[0]
            self.driver.switch_to.window(main)
            time.sleep(3)
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.css-18t94o4[data-testid ="confirmationSheetConfirm"]')))
            except:
                time.sleep(20)
            sleep_time = random.randint(10, 20)
            time.sleep(sleep_time)
            retweet_btn = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="confirmationSheetConfirm"]')
            retweet_btn.click()
            time.sleep(5)
            if self._check_status(status,url):
                flag = False
            else:
                sleep_time = random.randint(180, 460)
                print('sleeping.......' + str(sleep_time))
                time.sleep(sleep_time)


