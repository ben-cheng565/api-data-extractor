import json  # For JSON loading
import datetime

from fetch import fetch_data

def flatten_json(item, key=None, key_prefix=""):
    #add prefix to the column name, if the node is a json object
    if isinstance(item, dict):
        
        leaves = {}
        for item_key in item.keys():
            temp_key_prefix = (
                item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
            )
            leaves.update(flatten_json(item[item_key], item_key, temp_key_prefix))
        return leaves
    else:
        #format the date data
        if type(item) is str:
            if item.startswith('/Date'):
                timestamp = datetime.datetime.fromtimestamp(int(item[6:19])/1000)
                #print(timestamp)
                item = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return {key_prefix: item}


def split_json(data, category):
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



