import requests
import json

from config import api_url, secret_key, api_id
from signature import generate_signature

def fetch_data(table_name):
    try:
        api_headers = {
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
            'api-auth-id': api_id,
            'api-auth-signature': generate_signature('', secret_key)
            }
        response = requests.get(api_url + table_name, headers = api_headers)
        #response = requests.get(api_url)
        
    except:
        print("Connect api failed.")
    

    if response.status_code == 200:
        data = response.json()
       
        return data["Items"]
    else:
        print("Fetch data failed.")
        
#fetch_data()   
    
    
        