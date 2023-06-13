import datetime

def flatten_json(item, key=None, key_prefix=""):
    if isinstance(item, dict):
        leaves = {}
        for item_key in item.keys():
            temp_key_prefix = (
                item_key if (key_prefix == "") else (key_prefix + "_" + str(item_key))
            )
            leaves.update(flatten_json(item[item_key], item_key, temp_key_prefix))
        return leaves
    else:
        if type(item) is str and item.startswith('/Date'):
            timestamp = datetime.datetime.fromtimestamp(int(item[6:19])/1000)
            item = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return {key_prefix: item}

def split_json(data, category):
    main_json = [] 
    child_json = [] 
    child_key = ""  

    for item in data:
        for k, v in item.items():
            if isinstance(v, list):
                for l in v:
                    l.update({category + '_Guid': item['Guid']})
                    child_json.append(l)
                child_key = k
            
        del item[child_key]
        main_json.append(item)

    final_data = {}
    final_data.update({category: main_json})
    final_data.update({child_key: child_json})
    
    return final_data
