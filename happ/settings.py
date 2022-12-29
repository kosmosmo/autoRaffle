#from environs import Env
import os,json


root_path =os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+ '\\'
def _get_key():
    f = open(root_path + 'key.json')
    data = json.load(f)
    return data
data = _get_key()
capture = data["capture"]


CAPTCHA_RESOLVER_API_URL = 'https://api.yescaptcha.com/createTask'
CAPTCHA_RESOLVER_API_KEY =capture

CAPTCHA_DEMO_URL = 'https://democaptcha.com/demo-form-eng/hcaptcha.html'

CAPTCHA_ENTIRE_IMAGE_FILE_PATH = 'captcha_entire_image.png'
CAPTCHA_SINGLE_IMAGE_FILE_PATH = 'captcha_single_image_%s.png'
CAPTCHA_RESIZED_IMAGE_FILE_PATH = 'captcha_resized_image.png'
