from json_handler import split_json
from fetch import fetch_data
from write import write_csv

def main():
    #the category name needed to extract, value can be 'Invoices' or 'Customers'
    query_data = 'Invoices'
    json_data = split_json(fetch_data(query_data), query_data)
    #traverse data to store into csv file
    for k, v in json_data.items():
        write_csv(v, k)

if __name__ == "__main__":
    main()