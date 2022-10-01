import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,random
class twitterJobs():
    def __init__(self,retweet_links,follow_links):
        self.driver = self.get_driver()
        self.retweet_links = retweet_links
        self.follow_links = follow_links

    def get_driver(self):
        options = webdriver.ChromeOptions()
        time.sleep(2)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        time.sleep(2)
        options.add_argument(r'--profile-directory=Default')
        time.sleep(2)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def _check_status(self,status):
        if status == "followed":
            return self._check_followed()
        try:
            retweeted = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[data-testid ="{}"]'.format(status))
            if retweeted:
                return True
            return False
        except:
            return False

    def run(self):
        time.sleep(2)
        for item in self.follow_links:
            self.actions(item,"unretweet")
            self.actions(item, "unlike")

    def _check_followed(self):
        followed_btn = "css-18t94o4.css-1dbjc4n.r-1niwhzg.r-2yi16"
        time.sleep(5)
        try:
            elements = self.driver.find_elements(By.CLASS_NAME, followed_btn)
        except:
            elements = []
        return self._get_following_btn(elements)

    def _get_following_btn(self,elements):
        for item in elements:
            if item.text == "Following":
                return True
        return False

    def actions(self,url,status):
        #status "unretweet" for retweet
        #status "unlike" for like
        #status "followed" for follow
        flag = True
        while flag:
            self.driver.get(url)
            self.driver.maximize_window()
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.css-18t94o4[data-testid ="confirmationSheetConfirm"]')))
            except:
                time.sleep(20)
            retweet_btn = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="confirmationSheetConfirm"]')
            retweet_btn.click()
            time.sleep(10)
            if self._check_status(status):
                flag = False
            else:
                sleep_time = random.randint(20, 100)
                print('sleeping.......' + str(sleep_time))
                time.sleep(sleep_time)


a = twitterJobs(["https://twitter.com/intent/retweet?tweet_id=1566915113436827649",
                 "https://twitter.com/intent/retweet?tweet_id=1575581391504347136",
                 "https://twitter.com/intent/retweet?tweet_id=1531095577228091395",
                 ],
                ["https://twitter.com/intent/user?screen_name=DuelRealms&utm_source=alphabot.app",
                 "https://twitter.com/intent/user?screen_name=etofficialnft&utm_source=alphabot.app",
                 "https://twitter.com/intent/user?screen_name=theabysswtf&utm_source=alphabot.app",
                 "https://twitter.com/intent/user?screen_name=Machina_NFT&utm_source=alphabot.app"])
a.run()