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
        options.add_argument("start-maximized")
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory=Default')
        return webdriver.Chrome(options=options,use_subprocess=True)


    def run(self):
        self.driver.get("https://twitter.com/")
        self.follow()
        self.retweet()
        self.driver.close()
        self.driver.quit()

    def _check_followed(self):
        followed_btn = "css-18t94o4.css-1dbjc4n.r-1niwhzg.r-2yi16"
        time.sleep(5)
        elements = self.driver.find_elements(By.CLASS_NAME, followed_btn)
        followd = self._get_following_btn(elements)
        return followd

    def _get_follow_btn(self,elements):
        for item in elements:
            if item.text == "Follow":
                return item

    def _get_following_btn(self,elements):
        for item in elements:
            if item.text == "Following":
                return item

    def follow(self):
        follow_btn = "css-18t94o4.css-1dbjc4n.r-42olwf.r-2yi16"
        check_follow = "css-18t94o4.css-1dbjc4n"
        for link in self.follow_links:
            self.driver.get(link)
            timeout = 15
            try:
                element_present = EC.presence_of_element_located((By.CLASS_NAME, check_follow))
                WebDriverWait(self.driver, timeout).until(element_present)
            except TimeoutException:
                pass
            finally:
                pass
            time.sleep(5)
            checker = self._check_followed()
            while not checker:
                try:
                    elements = self.driver.find_elements(By.CLASS_NAME,
                                                 follow_btn
                                                 )
                    follow = self._get_follow_btn(elements)
                    follow.click()
                    time.sleep(5)
                    self.driver.refresh()
                    time.sleep(5)
                    checker = self._check_followed()
                    if not checker:
                        sleep_time = random.randint(120, 360)
                        print('sleeping.......' + str(sleep_time))
                        time.sleep(sleep_time)
                except:
                    self.driver.get(link)
                    time.sleep(5)
                    pass


    def _check_retweet(self):
        try:
            retweeted = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="unretweet"]')
        except:
            retweeted = None
        try:
            liked = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="unlike"]')
        except:
            liked = None
        return [retweeted,liked]

    def _retweet_action(self):
        self.driver.find_element(By.CSS_SELECTOR,
                                 '.css-18t94o4[data-testid ="retweet"]'
                                 ).click()
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.RETURN).perform()

    def _like_action(self):
        self.driver.find_element(By.CSS_SELECTOR,
                                 '.css-18t94o4[data-testid ="like"]'
                                 ).click()

    def retweet(self):
        for link in self.retweet_links:
            self.driver.get(link)
            timeout = 15
            try:
                element_present = EC.presence_of_element_located((By.CSS_SELECTOR,'.css-18t94o4[data-testid ="reply"]'))
                WebDriverWait(self.driver, timeout).until(element_present)
            except TimeoutException:
                pass
            finally:
                pass
            time.sleep(5)
            checker = self._check_retweet()
            while not checker[0] or not checker[1]:
                try:
                    if not checker[0]:
                        self._retweet_action()
                    if not checker[1]:
                        self._like_action()
                    time.sleep(10)
                    time.sleep(5)
                    self.driver.refresh()
                    time.sleep(5)
                    checker = self._check_retweet()
                    if not checker[0] or not checker[1]:
                        sleep_time = random.randint(120, 360)
                        print('sleeping.......' + str(sleep_time))
                        time.sleep(sleep_time)
                        self.driver.refresh()
                except:
                    self.driver.get(link)
                    time.sleep(5)

