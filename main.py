import os
from dotenv import load_dotenv

from api.api_data import ApiData
from utils.file_utils import write_csv

load_dotenv()

api_url = os.getenv("API_URL")
api_id = os.getenv("API_ID")
secret_key = os.getenv("SECRET_KEY")

api_data = ApiData(api_url, api_id, secret_key)

query_data = 'Invoices'
raw_data = api_data.fetch_data(query_data)
json_data = api_data.prepare_data(raw_data, query_data)

for k, v in json_data.items():
    write_csv(v, k)
