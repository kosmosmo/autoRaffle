import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import time,random,os
from urllib.parse import urlparse
from urllib.parse import parse_qs
import utils as u
import json,os
from airtable_wrapper import AirtableWrapper
#tw_cache = u.get_twitter_cache()
tw_cache = {
    "retweet":{},
    "follow":{}
}
root_path =  os.path.dirname(os.path.realpath(__file__)) + '\\'
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data['key']
key = _get_key()
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)

class twitterJobs():
    def __init__(self,retweet_links,follow_links,check_cache=True):

        self.retweet_links = retweet_links
        self.follow_links = follow_links
        self.check_cache = check_cache

    def on_start(self):
        self.driver = self.get_driver()
        time.sleep(2)
        self.driver.maximize_window()
        time.sleep(2)
        self.driver.get("https://www.google.com/")
        time.sleep(2)
        all_list = at_obj.get_all("black_list").get('records')
        self.black_list = u.get_black_list(all_list)

    def get_driver(self):
        options = webdriver.ChromeOptions()
        time.sleep(1)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        time.sleep(1)
        options.add_argument(r'--profile-directory=Default')
        time.sleep(1)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def _check_account_exit(self):
        try:
            checking = self.driver.find_element(By.CSS_SELECTOR,
                                                '.css-901oao[data-testid ="empty_state_header_text"]')
            if checking:
                return False
            return True
        except:
            return True

    def _check_status(self,status,url):
        time.sleep(5)
        account_exit = self._check_account_exit()
        if not account_exit:
            print("!!!!!!invalid links. Skipped.")
            print(url)
            return True
        try:
            if status == "followed":
                user = self._get_user_name(url)
                checking = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[aria-label ="Following @{}"]'.format(user))
                if checking and self.check_cache:
                    tw_cache["follow"][u.get_id(url).lower()] = ""
                    u._write_cache("tw_cache.json", tw_cache)
            else:
                checking = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[data-testid ="{}"]'.format(status))
                if checking and self.check_cache:
                    tw_cache["retweet"][u.get_id(url).lower()] = ""
                    u._write_cache("tw_cache.json", tw_cache)
            if checking:
                return True
            return False
        except:
            return False

    def run(self):
        self.on_start()
        time.sleep(2)
        for item in self.follow_links:
            if u.get_id(item) in self.black_list:
                continue
            if u.get_id(item) in tw_cache["follow"]:
                continue
            self.actions(item, "followed")
        for item in self.retweet_links:
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

    def check_limited(self,url):
        time.sleep(3)
        try:
            limited_btn = self.driver.find_element(By.CLASS_NAME, "Button.EdgeButton.EdgeButton--primary")
            if limited_btn:
                print ("account limited. Refreshing!")
                time.sleep(1)
                limited_btn.click()
                time.sleep(4)
                self.driver.refresh()
                time.sleep(4)
                self.driver.get(url)
        except:
            pass

    def actions(self,url,status):
        #status "unretweet" for retweet
        #status "unlike" for like
        #status "followed" for follow
        flag = True
        while flag:
            self.driver.get(url)
            time.sleep(2)
            main = self.driver.window_handles[0]
            self.driver.switch_to.window(main)
            self.check_limited(url)
            time.sleep(2)
            try:
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.css-18t94o4[data-testid ="confirmationSheetConfirm"]')))
            except:
                time.sleep(20)
            sleep_time = random.randint(3, 5)
            time.sleep(sleep_time)
            retweet_btn = self.driver.find_element(By.CSS_SELECTOR,'.css-18t94o4[data-testid ="confirmationSheetConfirm"]')
            retweet_btn.click()
            time.sleep(3)
            if self._check_status(status,url):
                flag = False
            else:
                sleep_time = random.randint(180, 460)
                print('sleeping.......' + str(sleep_time))
                time.sleep(sleep_time)

class twitterJobs_undo(twitterJobs):
    def __init__(self, retweet_links,follow_links,total=0):
        twitterJobs.__init__(self,retweet_links,follow_links)
        self.total = str(len(retweet_links) + len(follow_links))
        self.white_list = self.get_white_list()

    def get_white_list(self):
        all_list = at_obj.get_all("white_list").get('records')
        return u.get_white_list(all_list)

    def convert_url(self,url):
        if "screen_name=" in url:
            end = url.split("screen_name=")[-1]
            if "&" in end:
                end = end.split("&")[0]
            return "https://twitter.com/" + end
        if "tweet_id=" in url:
            end = url.split("tweet_id=")[-1]
            if "&" in end:
                end = end.split("&")[0]
            return "https://twitter.com/{}/status/".format("tttt") + end

    def run(self):
        self.on_start()
        time.sleep(2)
        i = 1
        for item in self.follow_links:
            print ("{}/{}".format(str(i),self.total))
            if u.get_id(item) in self.black_list:
                continue
            if u.get_id(item) in tw_cache["follow"]:
                continue
            self.actions(item, "followed")
            i += 1
        for item in self.retweet_links:
            print("{}/{}".format(str(i), self.total))
            if u.get_id(item) in tw_cache["retweet"]:
                continue
            self.actions(item,"unretweet")
            self.actions(self._convert_like_url(item), "unlike")
            i += 1
        self.driver.quit()

    def actions(self,url,status):
        #status "unretweet" for retweet
        #status "unlike" for like
        #status "followed" for follow

        flag = True
        while flag:
            new_url = self.convert_url(url)
            wl_skip = False
            for item in self.white_list:
                if item.lower() in new_url.lower():
                    wl_skip = True
                    break
            if status == "followed" and wl_skip:
                flag = False
            else:
                self.driver.get(new_url)
                time.sleep(3)
                main = self.driver.window_handles[0]
                self.driver.switch_to.window(main)
                self.check_limited(new_url)
                sleep_time = random.randint(5, 7)
                time.sleep(sleep_time)


                if status == "followed":
                    try:
                        user = self._get_user_name(url)
                        unfollow = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[aria-label ="Following @{}"]'.format(user))
                        unfollow.click()
                        time.sleep(2)
                        confirm_btn = self.driver.find_element(By.CSS_SELECTOR,
                                                               '.css-18t94o4[data-testid ="confirmationSheetConfirm"]')
                        confirm_btn.click()
                        time.sleep(1)
                    except:
                        pass
                else:
                    try:
                        unlike = self.driver.find_element(By.CSS_SELECTOR, '.css-18t94o4[data-testid ="{}"]'.format(status))
                        unlike.click()
                    except:
                        pass
                    time.sleep(2)
                    try:
                        unlikes = self.driver.find_elements(By.CLASS_NAME, 'css-901oao.css-16my406.r-poiln3.r-bcqeeo.r-qvutc0')
                        for item in unlikes:
                            if item.text == "Undo Retweet":
                                item.click()
                    except:
                        pass
                flag = False
