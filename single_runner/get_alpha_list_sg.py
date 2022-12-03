from airtable_wrapper import AirtableWrapper
import discum,json,pprint,sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
print (sys.path)
from alpha_obj import alpha_obj
from airtable_wrapper import AirtableWrapper
import undetected_chromedriver as webdriver
from selenium.webdriver.common.by import By
from urllib.parse import urlparse
from urllib.parse import parse_qs
from discum.utils.button import Buttoner
import time,datetime
import get_raffle_list as premint
import random
root_path = ""

def _get_keys():
    f = open(root_path + 'key_sg.json')
    data = json.load(f)
    return data
keys = _get_keys()
airtable_key = keys['airtable_key']
discord_token = keys['discord_token']
airtable_base_id = keys['airtable_base_id']

bot = discum.Client(token=discord_token, log=False)
msgs_history = []
at_obj = AirtableWrapper(airtable_base_id,airtable_key)
history_ct = 10

def get_twitter_machine():
    at_obj.get_all("twitter")
    tw_all = at_obj.get_all("twitter").get('records')
    res = []
    for item in tw_all:
        fields = item.get('fields')
        machine = fields.get('machine')
        res.append(machine)
    return res

def get_alpha_index():
    #machine_list = get_twitter_machine()
    index_list = at_obj.get_all("alpha index").get('records')
    for item in index_list:
        fields = item.get('fields')
        Name = fields.get("Name")
        print (Name)
        Channel_id = fields.get("Channel id")
        rid = item.get('id')
        skip = fields.get("skip")
        if skip:
            continue
        feed = bot.getMessages(Channel_id, history_ct)
        msgs_history = alpha_obj.alpha_base.convert_msgs(json.loads(feed.text))

        for item in msgs_history:
            urllow =  item.url.lower()
            tt = item.time.replace(" ","T") + ".000Z"
            end = item.time_remain
            if end and end.endswith(" hr"):
                check_time = int(end.split(" ")[0])
                if check_time < -1:
                    continue
            find_rec = at_obj.get("alpha list", filter_by_formula='FIND("{}", Url)'.format(urllow)).get(
                'records')
            #machine_pick = random.choice(machine_list)
            if not find_rec:
                at_obj.create("alpha list", {
                    "url":urllow,
                    "alpha index":[str(rid)],
                    "time":tt,
                    "end" : end,

                    "skip":True
                })
        time.sleep(1)

def _check_over(driver):
    try:
        over = driver.find_element(By.CLASS_NAME, 'MuiTypography-root.MuiTypography-h5')
        if "You're not a winner. Maybe next time!" in over.text or "You're a winner! Congratulations" in over.text or "Raffle is over." in over.text:
            return False
        return True
    except:
        return True


def clean_alpha_index():
    alpha_lists = at_obj.get_all("alpha list").get('records')
    for item in alpha_lists:
        fields = item.get('fields')
        url = fields.get('url')
        rid = item.get('id')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options, use_subprocess=True)
        driver.get(url)
        if not _check_over(driver):
            at_obj.delete("alpha list",rid)


def archive_raffles():
    alpha_lists = at_obj.get_all("alpha list").get('records')
    for item in alpha_lists:
        rid = item.get('id')
        fields = item.get('fields')
        url = fields.get('url')
        created_time = fields.get('created time')
        fail_count = fields.get('fail count')
        fail_reason = fields.get('fail reason','')
        discord = fields.get("Name (from alpha index)",["unknown"])[0]
        tt =  fields.get('time')
        created_date = created_time.split('T')[0]
        dt = datetime.datetime.strptime(created_date, "%Y-%m-%d")
        today = datetime.datetime.now()
        if abs((today - dt).days) > 2:
            at_obj.delete("alpha list",rid)
            time.sleep(0.2)

#def archive_premint():
#   raffle_lists = at_obj.get_all("raffle list").get('records')
#   for item in raffle_lists:
#       rid = item.get('id')
#       fields = item.get('fields')
#       status = fields.get("status",'')
#       if status == "Done" or status == "Nope":
#           at_archive.create("archive_premint",fields)
#           at_obj.delete("raffle list",rid)
#           time.sleep(0.2)

@bot.gateway.command
def monitoring(resp):
    global msgs_history
    if resp.event.ready_supplemental:
        get_alpha_index()
        #clean_alpha_index()
        #archive_raffles()
        #archive_premint()
        bot.gateway.close()

class dc_monitor():
    def runner(self):
        bot.gateway.run(auto_reconnect=True)

if __name__ == "__main__":
    dc_monitor_object = dc_monitor()
    dc_monitor_object.runner()
