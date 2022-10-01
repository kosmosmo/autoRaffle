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

    def follow(self,url):
        self.driver.get(url)
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.css-18t94o4[data-testid ="confirmationSheetConfirm"]')))
        except:
            time.sleep(20)
        retweet_btn = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="unretweet"]')
        retweet_btn.click()

a = twitterJobs([],[])
a.follow('https://twitter.com/intent/retweet?tweet_id=1566915113436827649')