import json
import csv

def json_to_csv(json_file,csv_file):
    with open(json_file,mode='r') as file:
        reader=json.load(file)
        

    # writing to csv
    with open (csv_file,mode='w') as file:
        fieldnames=reader[0].keys() #it means extract the key from dict which becomes the columns in csv
        writer=csv.DictWriter(file,fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(reader)
    
    # writing json to csv 
json_to_csv('data.json','new_data.csv')