from airtable_wrapper import AirtableWrapper
import discum,json,pprint
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
root_path = "C:\\Users\\kosmo\\PycharmProjects\\autoRaffle\\"

def _get_keys():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
keys = _get_keys()
key = keys['key']
token = keys['token']
bot = discum.Client(token=token, log=False)
msgs_history = []
at_obj = AirtableWrapper("appNj4kFlbJGa6IOm",key)
history_ct = 10
at_archive = AirtableWrapper("appo1xVFD4xpPmmGT",key)

def scroll_to_bottom(driver):

    old_position = 0
    new_position = None

    while new_position != old_position:
        # Get old scroll position
        old_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))
        # Sleep and Scroll
        time.sleep(1)
        driver.execute_script((
                "var scrollingElement = (document.scrollingElement ||"
                " document.body);scrollingElement.scrollTop ="
                " scrollingElement.scrollHeight;"))
        # Get new position
        new_position = driver.execute_script(
                ("return (window.pageYOffset !== undefined) ?"
                 " window.pageYOffset : (document.documentElement ||"
                 " document.body.parentNode || document.body);"))

url = 'https://docs.google.com/spreadsheets/d/15BnCMlO4gbrdV23z9BCIi-ekj_z8wd3tRIhLiaaHo5I/edit#gid=0'
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(options=options, use_subprocess=True)
driver.get(url)
time.sleep(2)
import pyautogui


res = {}
wals = at_obj.get_all("emails").get('records')
for w in wals:
    fields = w.get('fields')
    wallet1 = fields.get("wallet","")
    wallet2 = fields.get("wallet_mint","")
    name = fields.get("ID","")
    if wallet1:
        res[wallet1] = name
    if wallet2:
        res[wallet2] = name + "2"

for key,val in res.items():
    time.sleep(0.2)
    pyautogui.hotkey('ctrl', 'f')
    pyautogui.typewrite(key)
    pyautogui.hotkey('Return')
    time.sleep(0.8)
    if key.lower() in driver.page_source.lower():
       print (val)


