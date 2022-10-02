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
    return data['key']
key = _get_key()

at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)

class alphaJobs():
    def __init__(self,url):
        self.url = url
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

    def _find_error(self):
        errors = self.driver.find_elements(By.CLASS_NAME, 'MuiAlert-standardError')
        for item in errors:
            if "join" in item.text.lower() and "discord" in item.text.lower():
                find_rec = at_obj.get("alpha fails", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                    'records')
                if not find_rec:
                    at_obj.create("alpha fails",{
                        "Url":self.url,
                        "Notes":item.text
                    })
                return False
        return True

    def _get_raffle_requritement(self):
        retweet_links = set()
        follow_links = set()
        elems = self.driver.find_elements(by=By.XPATH, value="//a[@href]")
        for elem in elems:
            url = elem.get_attribute("href")
            print(url)
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
        reg_btn = self.driver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
        time.sleep(10)
        reg_btn.click()
        time.sleep(15)
        checker = self._find_error()
        if checker:
            req = self._get_raffle_requritement()
            self.driver.quit()
            tw_job = twitter_job.twitterJobs(req[0], req[1])
            tw_job.run()
            self.driver.get(self.url)
            time.sleep(10)
            reg_btn.click()
        self.driver.quit()



a = alphaJobs('https://www.alphabot.app/mc-nuos-wl-giveaway-yzeakj')
a.run()

b = alphaJobs('https://www.alphabot.app/tentacular-wl-giveaway-6nynn2')
b.run()

c = alphaJobs('https://www.alphabot.app/thegalanft-wl-giveaway-uaa1sk')
c.run()