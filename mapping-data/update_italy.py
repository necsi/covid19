import json
import csv
from datetime import datetime
​
now = datetime.now()
dt_string = now.strftime("%B %d,%Y %H:%M:%S")
​
italy={}
with open('italy.json') as json_file:
    data = json.load(json_file)
    italy=data
​
​
all_data={}
all_data["type"]="FeatureCollection"
all_data["features"]=[]
​
​
#ITA_adm1-1.json
with open('ne_count17.json') as json_file:
    data = json.load(json_file)
    for el in data["features"]:
        bb={}
        bb["type"]="Feature"
        bb["geometry"]={}
        bb["geometry"]["type"]=el["geometry"]["type"]
        bb["geometry"]["coordinates"]=el["geometry"]["coordinates"]
        bb["properties"]={}
        bb["properties"]["code"]=el["properties"]["code"]
        bb["properties"]["name"]=el["properties"]["name"]
        bb["properties"]["iso"]=el["properties"]["iso"]
        print(list(italy.keys()))
        bb["properties"]["woe_label"]=dt_string
        if bb["properties"]["name"] in list(italy.keys()):
            bb["properties"]["scalerank"]=italy[bb["properties"]["name"]]["scalerank"]
            bb["properties"]["one_day"]=italy[bb["properties"]["name"]]["one_day"]
        else:
            print(bb["properties"]["name"])
            bb["properties"]["scalerank"]=el["properties"]["scalerank"]
            bb["properties"]["one_day"]=el["properties"]["one_day"]
        all_data["features"].append(bb)
​
​
​
​
        
#print(all_data)
#{'ID_0': 112, 'ISO': 'ITA', 'NAME_0': 'Italy', 'ID_1': 20, 'NAME_1': 'Veneto', 'TYPE_1': 'Regione', 'ENGTYPE_1': 'Region', 'NL_NAME_1': '', 'VARNAME_1': 'Venecia|Venetia|Venezia Euganea'}
#print(all_data)            
with open('ne_count25.json', 'w') as outfile:
    json.dump(all_data, outfile)