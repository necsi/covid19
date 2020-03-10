import json
import csv
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%B %d,%Y %H:%M:%S")


all_data0={}
ddata=[]
with open('data1.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     ddata=[]
     for row in reader:
          if ", " not in row["Province/State"]:
              ddata.append(row) 
              #print(row["Province/State"])               
              all_data0[row["Province/State"]]={}
              dates=list(row.keys())[4:]
              for el in dates:
                   all_data0[row["Province/State"]][el]=[]
                   
              '''
              dates=list(row.keys())[4:]
              for el in dates:
                  all_data[row["Province/State"].split(", ")[1].replace(" (From Diamond Princess)","")][el]=row[el]
              '''
     #print(all_data0)         
     for row in ddata:
          #print(row)
          dates2=list(row.keys())[4:]
          #print(row,dates2)
          for el in dates2:
               all_data0[row["Province/State"]][el].append(int(row[el]))
print(all_data0.keys())


#dict_keys(['WA', 'IL', 'AZ', 'ON', 'CA', 'MA', 'WI', 'TX', 'NE', 'QC', 'OR', 'RI', 'NH', 'FL', 'NY'])
kkeys={'WA':'Washington', 'IL':'Illinois', 'AZ':'Arizona', 'ON':'Ontario', 'CA':'California', 'MA':'Massachusetts', 'WI':'Wyoming', 'TX':'Texas', 'NE':'Nebraska', 'QC':'Quebec', 'OR':'Oregon','RI':'Rhode Island', 'NH':'New Hampshire','FL':'Florida','NY':'New York','GA':'Georgia','NC':'North Carolina'}
all_data=all_data0





#OrderedDict([('Province/State', 'Providence, RI'), ('Country/Region', 'US'), ('Lat', '41.824'), ('Long', '-71.4128'), ('1/22/20', '0'), ('1/23/20', '0'), ('1/24/20', '0'), ('1/25/20', '0'), ('1/26/20', '0'), ('1/27/20', '0'), ('1/28/20', '0'), ('1/29/20', '0'), ('1/30/20', '0'), ('1/31/20', '0'), ('2/1/20', '0'), ('2/2/20', '0'), ('2/3/20', '0'), ('2/4/20', '0'), ('2/5/20', '0'), ('2/6/20', '0'), ('2/7/20', '0'), ('2/8/20', '0'), ('2/9/20', '0'), ('2/10/20', '0'), ('2/11/20', '0'), ('2/12/20', '0'), ('2/13/20', '0'), ('2/14/20', '0'), ('2/15/20', '0'), ('2/16/20', '0'), ('2/17/20', '0'), ('2/18/20', '0'), ('2/19/20', '0'), ('2/20/20', '0'), ('2/21/20', '0'), ('2/22/20', '0'), ('2/23/20', '0'), ('2/24/20', '0'), ('2/25/20', '0'), ('2/26/20', '0'), ('2/27/20', '0'), ('2/28/20', '0'), ('2/29/20', '0'), ('3/1/20', '1')])



json_file0={}
json_file0["type"]="FeatureCollection"
json_file0["features"]=[]

with open('ne_count16.json') as json_file:
    data = json.load(json_file)
    for elem in data["features"]:
        #if "Antarctica" not in elem["properties"]["name"]:
         bb={}
         bb["type"]="Feature"
         bb["geometry"]={}
         bb["geometry"]["type"]=elem["geometry"]["type"]
         bb["geometry"]["coordinates"]=elem["geometry"]["coordinates"]
         bb["properties"]={}
         bb["properties"]["iso"]=elem["properties"]["iso"]
         bb["properties"]["name"]=elem["properties"]["name"]
         bb["properties"]["code"]=elem["properties"]["code"]
         #bb["properties"]["longitude"]=elem["properties"]["longitude"]
         #bb["properties"]["latitude"]=elem["properties"]["latitude"]
         if elem["properties"]["name"] in list(all_data.keys()):
              bb["properties"]["woe_label"]=dt_string
              #print(all_data[elem["properties"]["NAME_1"]]['2/29/20'])
              #bb["properties"]["min_zoom"]=all_data[elem["properties"]["NAME_1"]]['2/29/20']
              bb["properties"]["scalerank"]=sum(all_data[elem["properties"]["name"]]['3/9/20'])
              bb["properties"]["one_day"]=sum(all_data[elem["properties"]["name"]]['3/9/20'])-sum(all_data[elem["properties"]["name"]]['3/8/20'])
         else:
              #bb["properties"]["min_zoom"]=0
              bb["properties"]["woe_label"]=elem["properties"]["woe_label"]
              bb["properties"]["scalerank"]=elem["properties"]["scalerank"]
              bb["properties"]["one_day"]=elem["properties"]["one_day"]
            #elem["properties"]["scalerank"]
         json_file0["features"].append(bb)
#print(json_file0)          
with open('ne_count17.json', 'w') as outfile:
    json.dump(json_file0, outfile)            

