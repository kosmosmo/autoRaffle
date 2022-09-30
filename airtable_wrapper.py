import airtable,collections,time,requests,json,pprint
class AirtableWrapper(airtable.Airtable):
    def __init__(self, base_id, api_key):
        super().__init__(base_id, api_key)
        self.base_id = base_id
        self.api_key = api_key

    def get_all(
                self, table_name, record_id=None, limit=0, offset=None,
                filter_by_formula=None, view=None, max_records=0, fields=[]):
        res = []
        get_data = self.get(table_name, record_id=record_id, limit=limit, offset=offset,
                filter_by_formula=filter_by_formula, view=view, max_records=max_records, fields=fields)
        res+=get_data.get('records')
        offset_data = get_data.get('offset')
        i = 0
        while offset_data:
            print ('flipping pages: ' + str(i))
            get_data = self.get(table_name, record_id=record_id, limit=limit, offset=offset_data,
                filter_by_formula=filter_by_formula, view=view, max_records=max_records, fields=fields)
            res += get_data.get('records')
            offset_data = get_data.get('offset')
            i+= 1
            time.sleep(1)
        return collections.OrderedDict([('records',res)])

    def search(self,table_name,field_name,field_value,id=False):
        searcher = self.get(table_name,filter_by_formula=field_name+"=\"" + field_value + "\"").get(
                    'records')
        if searcher:
            search_value = searcher[0].get('fields')
        else:search_value = None
        if not id:
            return search_value
        else:
            return searcher[0]

    def find_table_id(self, name):
        url = "https://api.airtable.com/v0/meta/bases/{}/tables".format(self.base_id)
        headers = {
            'Authorization': f'Bearer ' + self.api_key,
            'Content-Type': 'application/json'
        }
        r = requests.get(url=url, headers=headers)
        data = json.loads(r.text)
        tables = data.get('tables')
        if tables:
            for table in tables:
                if table.get("name") == name:
                    return table.get("id")
        return None


