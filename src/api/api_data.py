import hashlib
import hmac
import base64
import requests
from utils.json_utils import flatten_json, split_json

class ApiData:
    def __init__(self, url, api_id, secret_key):
        self.url = url
        self.api_id = api_id
        self.secret_key = secret_key

    def generate_signature(self, query):
        message = bytes('', 'utf-8')
        secret = bytes(self.secret_key, 'utf-8')
        signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())
        return signature

    def fetch_data(self, table_name):
        api_headers = {
            'Content-Type' : 'application/json',
            'Accept': 'application/json',
            'api-auth-id': self.api_id,
            'api-auth-signature': self.generate_signature('')
            }
        response = requests.get(self.url + table_name, headers = api_headers)
            
        if response.status_code == 200:
            return response.json()["Items"]
        else:
            print("Fetch data failed.")
            return []

    def prepare_data(self, data, category):
        return split_json(data, category)
