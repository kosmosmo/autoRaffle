

class alphaJobs():
    def __init__(self,url,keyword,rid):
        self.url = url
        self.keyword= keyword
        self.rid = rid


    def on_start(self):
        self.driver = self.get_driver()
        time.sleep(2)
        self.driver.maximize_window()
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
                if len(self.driver.window_handles) >=3:
                    loaded = True
        time.sleep(5)


    def get_driver(self,profile="Default"):
        options = webdriver.ChromeOptions()
        options.add_argument(self.url)
        options.add_argument(r"user-data-dir=C:\Users\\Administrator\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory='+profile)
        return webdriver.Chrome(options=options,use_subprocess=True)

    def write_cache(self):
        cache = _get_cache()
        cache[self.url] = ""
        _write_cache(cache)

    def run(self):
        self.on_start()
        while len(self.driver.window_handles) >=3:
            time.sleep(5)
            self.driver.quit()
            time.sleep(5)
            self.on_start()

        self._click_reg()
        self.driver.quit()
        #if profiles:
        #    for item in profiles:
        #        auto_clean_pref(item,"pref\\"+item)
        #    p = profileJob(self.url,profiles)
        #    p.run()
        self.write_cache()


    def _check_over(self):
        try:
            over = self.driver.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-h5')
            if "You're not a winner. Maybe next time!" in over.text or "You're a winner! Congratulations" in over.text or "Raffle is over." in over.text:
                return False
            return True
        except:
            return True

    def _check_captcha(self):
        try:
            over = self.driver.find_element(By.CLASS_NAME, 'g-recaptcha-response')
            if over:
                return True
            return False
        except:
            return False

    def _find_error(self):
        errors = self.driver.find_elements(By.CLASS_NAME, 'MuiAlert-standardError')
        for item in errors:
            if "join" in item.text.lower() and "discord" in item.text.lower() and self.keyword.lower() not in item.text.lower():
                find_rec = at_obj.get("alpha list", filter_by_formula='FIND("{}", Url)'.format(self.url)).get(
                    'records')
                if find_rec:
                    rid = find_rec[0].get('id')
                    fail =  find_rec[0].get('fields').get('fail reason', "")
                    if not fail or fail == "unknow":
                        at_obj.update("alpha list", rid, {"fail reason": item.text})
                return False
        return True

    def _check_success_reg(self):
        time.sleep(4)
        try:
            checking = self.driver.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-h5.css-uz8pyt')
        except:
            return False
        if checking:
            return True
        return False

    def get_raffle_requritement(self):
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
                if "?" in user:
                    user = user.split("?")[0]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
            elif "tweet_id=" in url:  # alpha retweet
                tweet_id = url.split("tweet_id=")[-1]
                if "?" in tweet_id:
                    tweet_id = tweet_id.split("?")[0]
                retweet_links.add("https://twitter.com/intent/retweet?tweet_id=" + tweet_id)
            elif "/status/" in url:  # premint retweet
                tweet_id = url.split("/status/")[1]
                if "?" in tweet_id:
                    tweet_id = tweet_id.split("?")[0]
                retweet_links.add("https://twitter.com/intent/retweet?tweet_id=" + tweet_id)
            elif url not in filter_out:  # premint follow
                user = url.split("https://twitter.com/")[1]
                if "?" in user:
                    user = user.split("?")[0]
                follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
        return [self.remove_case_insenstive(list(retweet_links)), self.remove_case_insenstive(list(follow_links))]

    def remove_case_insenstive(self,org_list):
        res = []
        marker = set()
        for item in org_list:
            item_low = item.lower()
            if item_low not in marker:
                marker.add(item_low)
                res.append(item)
        return res

    #def _get_raffle_requritement(self):
    #    retweet_links = set()
    #    follow_links = set()
    #    elems = self.driver.find_elements(by=By.XPATH, value="//a[@href]")
    #    for elem in elems:
    #        url = elem.get_attribute("href")
    #        if not url.startswith("https://twitter.com/"):
    #            continue
    #        if "screen_name=" in url:  # alpha follow
    #            parsed_url = urlparse(url)
    #            user = parse_qs(parsed_url.query)['screen_name'][0]
    #            if "?" in user:
    #                user = user.split("?")[0]
    #            follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
    #        elif "like?" in url and "tweet_id=" in url:  # alpha like
    #            url = url.replace("like?","retweet?")
    #            retweet_links.add(url)
    #        elif "tweet_id=" in url:  # alpha retweet
    #            retweet_links.add(url)
    #        elif "/status/" in url:  # premint retweet
    #            tweet_id = url.split("/status/")[1]
    #            retweet_links.add("https://twitter.com/intent/retweet?tweet_id=" + tweet_id)
    #        elif url not in filter_out:  # premint follow
    #            user = url.split("https://twitter.com/")[1]
    #            if "?" in user:
    #                user = user.split("?")[0]
    #            follow_links.add("https://twitter.com/intent/user?screen_name=" + user)
    #        return [self.remove_case_insenstive(list(retweet_links)), self.remove_case_insenstive(list(follow_links))]

    def remove_case_insenstive(self,org_list):
        res = []
        marker = set()
        for item in org_list:
            item_low = item.lower()
            if item_low not in marker:
                marker.add(item_low)
                res.append(item)
        return res

    def _click_reg(self):
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
        time.sleep(2)
        reg_btn.click()
        time.sleep(10)
        checker = self._find_error()
        if checker:
            if self._check_success_reg():
                self.driver.quit()
                return
            req = self.get_raffle_requritement()
            self.driver.quit()
            tw_job = twitter_job.twitterJobs(req[0], req[1], check_cache=False)
            tw_job.run()
            time.sleep(1)
            self.driver = self.get_driver()
            time.sleep(6)
            try:
                reg_btn_new = self.driver.find_element(By.CSS_SELECTOR,
                                                   '.MuiButton-root[data-action ="view-project-register"]')
                reg_btn_new.click()
                time.sleep(10)
                self.driver.quit()

                tw_job = twitter_job.twitterJobs_undo(req[0], req[1])
                tw_job.run()
                self.driver.quit()
            except:
                pass

            time.sleep(2)


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
        self.driver.quit()
