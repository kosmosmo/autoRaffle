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
filter_out = [
    "https://twitter.com/premint_nft",
    "https://twitter.com/AlphabotApp"
]

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
        self.click_reg()

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

    def find_error(self):
        errors = self.driver.find_elements(By.CLASS_NAME, 'MuiAlert-standardError')
        for item in errors:
            print (item.text)
        time.sleep(30)

    def click_reg(self):
        reg_btn = self.driver.find_element(By.CSS_SELECTOR, '.MuiButton-root[data-action ="view-project-register"]')
        time.sleep(5)
        reg_btn.click()
        time.sleep(10)
        self.find_error()

a = alphaJobs('https://www.alphabot.app/mc-nuos-wl-giveaway-yzeakj')
a.run()

