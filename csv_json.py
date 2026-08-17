import csv
import json
def csv_to_json(csv_file,json_file):
    with open (csv_file,mode='r') as file:
        reader=csv.DictReader(file)
        data=[row for row in reader]
    # write the data to json 
    with open (json_file,mode='w') as file:
        json.dump(data,file,indent=4)
csv_to_json('data.csv','data.json')
