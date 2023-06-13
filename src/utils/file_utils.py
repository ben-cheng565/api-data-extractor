import csv
from utils.json_utils import flatten_json

def write_csv(data, file_name):
    csv_file = "files/" + file_name + ".csv"
    csv_columns = set()

    for d in data:
        csv_columns.update(flatten_json(d).keys())

    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = csv_columns)
        writer.writeheader()
        writer.writerows(flatten_json(entry) for entry in data)
