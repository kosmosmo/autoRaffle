from airtable_wrapper import AirtableWrapper
import discum,json,pprint
from alpha_obj import alpha_obj
from discum.utils.button import Buttoner
import time
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



def get_alpha_index():
    index_list = at_obj.get_all("alpha index").get('records')
    for item in index_list:
        fields = item.get('fields')
        Name = fields.get("Name")
        print (Name)
        Channel_id = fields.get("Channel id")
        rid = item.get('id')
        feed = bot.getMessages(Channel_id, history_ct)
        msgs_history = alpha_obj.alpha_base.convert_msgs(json.loads(feed.text))
        for item in msgs_history:
            urllow =  item.url.lower()
            find_rec = at_obj.get("alpha list", filter_by_formula='FIND("{}", Url)'.format(urllow)).get(
                'records')
            if not find_rec:
                at_obj.create("alpha list", {
                    "url":urllow,
                    "alpha index":[str(rid)]
                })
        time.sleep(5)


@bot.gateway.command
def monitoring(resp):
    global msgs_history
    if resp.event.ready_supplemental:
        get_alpha_index()


class dc_monitor():
    def runner(self):
        bot.gateway.run(auto_reconnect=True)


if __name__ == "__main__":
    dc_monitor_object = dc_monitor()
    dc_monitor_object.runner()