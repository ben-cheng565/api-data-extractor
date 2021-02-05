import hashlib
import hmac
import base64
import requests
import csv  # For CSV dict writer
import json  # For JSON loading
import datetime

class ApiData:
    def __init__(self, url, api_id, secret_key):
        self.url = url
        self.api_id = api_id
        self.secret_key = secret_key

    def generate_signature(self, query, private_key):
        message = bytes('', 'utf-8')
        secret = bytes('30bCvZwi4Tna25OJEnpUv6s7t3npfNWJxKD5HjeqYmBEKbnKBfDEjBbWELDDBUedUepSyMdGAwB4VUs2KQ==', 'utf-8')

        signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
        return signature

    def fetch_data(self, table_name):
        try:
            api_headers = {
                'Content-Type' : 'application/json',
                'Accept': 'application/json',
                'api-auth-id': self.api_id,
                'api-auth-signature': self.generate_signature('', self.secret_key)
                }
            response = requests.get(self.api_url + table_name, headers = api_headers)
            #response = requests.get(api_url)
            
        except:
            print("Connect api failed.")
            return []
        

        if response.status_code == 200:
            data = response.json()
        
            return data["Items"]
        else:
            print("Fetch data failed.")


    def flatten_json(self, item, key=None, key_prefix=""):
        #add prefix to the column name, if the node is a json object
        if isinstance(item, dict):
            
            leaves = {}
            for item_key in item.keys():
                temp_key_prefix = (
                    item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
                )
                leaves.update(self.flatten_json(item[item_key], item_key, temp_key_prefix))
            return leaves
        else:
            #format the date data
            if type(item) is str:
                if item.startswith('/Date'):
                    timestamp = datetime.datetime.fromtimestamp(int(item[6:19])/1000)
                    #print(timestamp)
                    item = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            return {key_prefix: item}


    def split_json(self, data, category):
        main_json = [] 
        child_json = [] 
        child_key = ""  

        for item in data:
            for k, v in item.items():
                # if the node is a list type
                if isinstance(v, list):
                    #then traverse all the items in the list
                    for l in v:
                        #append the parent guid to each child item
                        l.update({category + '_Guid': item['Guid']})
                        
                        child_json.append(l)
                    child_key = k
                    
                else:
                    continue
            #remove the list nodes from the parent json
            del item[child_key]
            #store the new parent json in main_json
            main_json.append(item)
        
        #union and return 
        final_data = {}
        final_data.update({category: main_json})
        final_data.update({child_key: child_json})
        
        return final_data

    def write_csv(self, data, file_name):
        #generate file name according to the category name
        csv_file = "files/" + file_name + ".csv"
        csv_columns = set()

        #extract column names from the json keys
        for d in data:
            csv_columns.update(self.flatten_json(d).keys())

        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
            writer.writeheader()
            writer.writerows(self.flatten_json(entry) for entry in data)


    
#####################class instance#####################
api_url = "https://api.unleashedsoftware.com/"
api_id = 'cfd50b0f-27c9-4b9e-a375-5088f63f6e61'
secret_key = '30bCvZwi4Tna25OJEnpUv6s7t3npfNWJxKD5HjeqYmBEKbnKBfDEjBbWELDDBUedUepSyMdGAwB4VUs2KQ=='

api_data = ApiData(api_url, api_id, secret_key)

#the category name needed to extract, value can be 'Invoices' or 'Customers'
query_data = 'Invoices'
json_data = api_data.split_json(api_data.fetch_data(query_data), query_data)
#traverse data to store into csv file
for k, v in json_data.items():
    api_data.write_csv(v, k)
