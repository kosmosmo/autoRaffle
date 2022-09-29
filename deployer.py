import urllib.request
import zipfile
zip = "https://github.com/kosmosmo/autoRaffle/archive/refs/heads/master.zip"
dir = r"C:\Users\kosmo\Desktop\doccc\bot.zip"
base_dir = r"C:\Users\kosmo\Desktop\doccc"
urllib.request.urlretrieve(zip, dir)
with zipfile.ZipFile(dir, 'r') as zip_ref:
    zip_ref.extractall(base_dir)