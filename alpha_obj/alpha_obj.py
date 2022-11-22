import pprint
import re
import datetime
class alpha_base():
    def __init__(self,m):
        self.m = m
        self.channelID = m['channel_id']
        self.guildID = m['guild_id'] if 'guild_id' in m else None
        self.channelID = m['channel_id']
        self.username = m['author']['username']
        self.discriminator = m['author']['discriminator']
        self.content = m['content']
        self.message_id = m['id']
        self.embeds = m['embeds']
        self.button = m.get('components')
        self.attachments = m.get('attachments')
        self.components = m.get('components')
        self.flags = m.get('flags')
        self.type = "base"
        self.time = ""
        self.time_remain = ""

    @staticmethod
    def get_alpha_type(meta_data):
        if not  meta_data.get('components'):
            return
        if meta_data.get('components'):
            comp = meta_data['components']
            try:
                label =comp[0]['components'][0]['label']
            except:
                label = None
            if label == "ENTER RAFFLE":
                url =comp[0]['components'][1]['url']
                return alpha_job(meta_data,url)
        else:
            return alpha_text_job(meta_data)
        return alpha_base(meta_data)

    @staticmethod
    def convert_msgs(msg_history):
        res = []
        for msg in msg_history:
            alpha_obj = alpha_base.get_alpha_type(msg)
            if not alpha_obj:
                continue
            if alpha_obj.type == "job":
                res.append(alpha_obj)
        return res


class alpha_job(alpha_base):
    def __init__(self,m,url):
        alpha_base.__init__(self,m)
        self.type = "job"
        self.url = url
        self.end = self.get_time()
        self.time = str(self.end)
        self.get_time_left()

    def get_time(self):
        if self.embeds:
            emb = self.embeds[0]
            fields = emb.get("fields",[])
            for item in fields:
                name = item.get('name')
                if name == "Ends":
                    value = item.get("value")
                    time = value.split("<t:")[1]
                    time = time.split(">")[0]
                    return  datetime.datetime.fromtimestamp( int(time) )
        return ""

    def get_time_left(self):
        now = datetime.datetime.now()
        self.time_remain = str(int((self.end - now).total_seconds()//3600)) + " hr"





class alpha_text_job(alpha_base):
    def __init__(self,m,):
        alpha_base.__init__(self,m)
        self.type = "text"
        content = m.get('content')
        urls = re.findall(r'(https?://[^\s]+)', content)
        for item in urls:
            if item.startswith("https://www.alphabot.app/"):
                self.url = item
                self.type = "job"
                break


