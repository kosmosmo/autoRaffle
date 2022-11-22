import etherscan,json,os
import time
def _get_key():
    f = open('../../key.json')
    data = json.load(f)
    return data
data = _get_key()
es_key = data["es_key"]

class tx_index():
    def __init__(self,contract,method_id):
        self.es = etherscan.Client(
            api_key=es_key,
            cache_expire_after=5,
        )
        self.contract = contract
        self.cache = self._load_cache()
        self.method_id = method_id
        self.new_indexing()



    def _load_cache(self):
        f = open(os.path.dirname(os.path.realpath(__file__)) + '\\index_cache.json')
        data = json.load(f)
        return data

    def _write_cache(self,data,file = '\\index_cache.json'):
        with open(os.path.dirname(os.path.realpath(__file__)) + file, "w") as outfile:
            json.dump(data, outfile, indent=4)

    def _add_to_hash_index(self,new_data,old_data):
        if new_data.get('input', "").startswith(self.method_id) and new_data.get("tx_receipt_status",False) == True:
            from_add = new_data.get('from', "")
            tx_hash = new_data.get('hash', "")
            if from_add not in old_data:
                old_data[from_add] = {tx_hash:""}
            else:
                old_data[from_add][tx_hash] = ""
        return old_data

    def new_indexing(self):
        if self.contract not in self.cache:
            all_tx = self._get_all_tx()
            cache_data = {
                "last_block":all_tx[-1]["block_number"],
                "hash_index":{}
            }
            for item in all_tx:
                temp = cache_data["hash_index"]
                cache_data["hash_index"] = self._add_to_hash_index(item,temp)
            self.cache[self.contract] = cache_data
            self._write_cache(self.cache)

    def transfer_count(self):
        res = {2:[],3:[],4:[]}
        for key,val in self.cache[self.contract]["hash_index"].items():
            if len(val) == 2:
                res[2].append(key)
            elif len(val) == 3:
                res[3].append(key)
            elif len(val) > 3:
                res[4].append(key)
        self._write_cache(res,file = "\\result.json")
        return res


    def _get_all_tx(self,start_block=0):
        flag = False
        i = 1
        res = []
        while not flag:
            txs = self.es.get_transactions_by_address(self.contract,page = i,start_block=start_block)
            res += txs
            i += 1
            if not txs:
                flag = True
            time.sleep(0.5)
        return res

    def add_indexing(self):
        new_tx = self._get_all_tx(start_block=self.cache[self.contract]["last_block"])
        if new_tx:
            self.cache[self.contract]["last_block"] = new_tx[-1]["block_number"]
        print_flag = False
        for item in new_tx:
            temp = self.cache[self.contract]["hash_index"]
            self.cache[self.contract]["hash_index"] = self._add_to_hash_index(item, temp)
            if temp !=  self.cache[self.contract]["hash_index"]:
                print_flag = True
        self._write_cache(self.cache)
        return print_flag



    def scaning_new_tx(self):
        while True:
            try:
                print_flag = self.add_indexing()

                res = self.transfer_count()
                print (res)
                time.sleep(5)
                continue
                #if res[2] and print_flag:
                #    print ("found duplicated mint: " + str(len(res[2])))
                #    print (list(res[2])[0])
                #if res[3] and print_flag:
                #    print ("found triplicated mint: " + str(len(res[3])))
                #    print(list(res[3])[0])
                #if res[4] and print_flag:
                #    print ("found multiple mint: " + str(len(res[4])))
                #
                #time.sleep(5)
            except:
                pass

if __name__ == "__main__":
    a = tx_index('0x6c869a43a9d362ef870d75dae56a01887578421d','0x1249c58b')
    print (a.transfer_count())
    a.scaning_new_tx()