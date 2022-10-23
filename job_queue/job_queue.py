import datetime,os,sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import alpha_sel_q as alpha_runner
import premint_sel_q as premint_runner
import time
def convert_to_airtable_time(date_time):
    at_time =  date_time.strftime("%Y-%m-%d %H:%M:%S")
    return at_time

class job_queue():
    def __init__(self,res):
        self.res = res

    def sort(self):
        self.res = sorted(self.res,key=lambda x:x.close_time)

    def run(self):
        i = 1
        for item in self.res:
            self.auto_clean_pref()
            print (str(i) + '/' + str(len(self.res)))
            print (item)
            tried = 0
            while tried < 3:
                try:
                    item.run()
                    tried = 4
                except:
                    tried += 1
            i += 1

    def auto_clean_pref(self):
        bad_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences.bad'
        pref_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
        if os.path.exists(bad_file_path) and os.path.getsize(bad_file_path) > 100000:
            os.remove(bad_file_path)
            print("deleted bad pref!!")
            time.sleep(5)
        if os.path.exists(pref_file_path) and os.path.getsize(pref_file_path) > 100000:
            try:
                self.clean_pref()
                print("clean pref!!")
            except:
                pass
            time.sleep(5)

    def clean_pref(self):
        pref_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
        to_address = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\Preferences"
        import shutil
        shutil.copyfile(to_address, pref_file_path)


class base_job():
    def __init__(self,close_time):
        self.close_time = close_time


class alpha_job(base_job):
    def __init__(self,close_time,url,keyword,rid):
        base_job.__init__(self,close_time)
        self.type = "alpha"
        self.rid = rid
        self.twitter_job = alpha_runner.alphaJobs(url,keyword,rid)
        if not self.close_time:
            self.close_time = datetime.datetime.now() + datetime.timedelta(hours=1)
            self.close_time = convert_to_airtable_time(self.close_time)
        else:
            self.close_time = self.close_time.replace('T',' ')[:-5]

    def __repr__(self):
        return self.close_time + " " + self.type + " " + self.rid

    def run(self):
        self.twitter_job.run()

class premint_job(base_job):
    def __init__(self,close_time,rid,retweet_links,follow_links):
        base_job.__init__(self,close_time)
        self.rid = rid
        self.type = "premint"
        self.twitter_job = premint_runner.premintJobs(rid,retweet_links,follow_links)
        self.convert_time()

    def convert_time(self):
        if not self.close_time:
            self.close_time = datetime.datetime.now() + datetime.timedelta(hours=24)
            self.close_time = convert_to_airtable_time(self.close_time)
        else:
            self.close_time = self.close_time.replace('T',' ')[:-5]

    def __repr__(self):
        return self.close_time + " " + self.type + " " + self.rid

    def run(self):
        self.twitter_job.run()