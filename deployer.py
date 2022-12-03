import urllib.request
import zipfile
print ('test.......................!!')
zip = "https://github.com/kosmosmo/autoRaffle/archive/refs/heads/master.zip"
dir = r"C:\Users\Administrator\Desktop\bot.zip"
base_dir = r"C:\Users\Administrator\Desktop"
urllib.request.urlretrieve(zip, dir)
with zipfile.ZipFile(dir, 'r') as zip_ref:
    zip_ref.extractall(base_dir)
import time

def clean_pref():
    pref_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    to_address = "C:\\Users\\Administrator\\Desktop\\autoRaffle-master\\Preferences"
    import shutil
    shutil.copyfile(to_address, pref_file_path)

def delet_bad_pref():
    import os
    bad_file_path = r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences.bad'
    pref_file_path =  r'C:\Users\Administrator\AppData\Local\Google\Chrome\User Data\Default\Preferences'
    if os.path.exists(bad_file_path):
        os.remove(bad_file_path)
        print ("deleted bad pref!!")
        time.sleep(5)
    if os.path.exists(pref_file_path):
        try:
            clean_pref()
            print("clean pref!!")
        except:
            pass
        time.sleep(5)


delet_bad_pref()