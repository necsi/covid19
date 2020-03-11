import json
import csv
from datetime import datetime

now = datetime.now()
dt_string = now.strftime("%B %d,%Y %H:%M:%S")


all_data={}
ddata=[]
with open('data1.csv', newline='') as csvfile:
     reader = csv.DictReader(csvfile)
     ddata=[]
     for row in reader:
          if row["Province/State"]=="":
              ddata.append(row) 
              #print(row["Province/State"])               
              all_data[row["Country/Region"]]={}
              dates=list(row.keys())[4:]
              for el in dates:
                   all_data[row["Country/Region"]][el]=[]
                   
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
               all_data[row["Country/Region"]][el].append(int(row[el]))

print(all_data)
#print(all_data["Åland"])


#dict_keys(['WA', 'IL', 'AZ', 'ON', 'CA', 'MA', 'WI', 'TX', 'NE', 'QC', 'OR', 'RI', 'NH', 'FL', 'NY'])
kkeys={'WA':'Washington', 'IL':'Illinois', 'AZ':'Arizona', 'ON':'Ontario', 'CA':'California', 'MA':'Massachusetts', 'WI':'Wyoming', 'TX':'Texas', 'NE':'Nebraska', 'QC':'Quebec', 'OR':'Oregon','RI':'Rhode Island', 'NH':'New Hampshire','FL':'Florida','NY':'New York'}
'''
all_data={}
for el in all_data0.keys():
     all_data[kkeys[el]]=all_data0[el]
'''



#OrderedDict([('Province/State', 'Providence, RI'), ('Country/Region', 'US'), ('Lat', '41.824'), ('Long', '-71.4128'), ('1/22/20', '0'), ('1/23/20', '0'), ('1/24/20', '0'), ('1/25/20', '0'), ('1/26/20', '0'), ('1/27/20', '0'), ('1/28/20', '0'), ('1/29/20', '0'), ('1/30/20', '0'), ('1/31/20', '0'), ('2/1/20', '0'), ('2/2/20', '0'), ('2/3/20', '0'), ('2/4/20', '0'), ('2/5/20', '0'), ('2/6/20', '0'), ('2/7/20', '0'), ('2/8/20', '0'), ('2/9/20', '0'), ('2/10/20', '0'), ('2/11/20', '0'), ('2/12/20', '0'), ('2/13/20', '0'), ('2/14/20', '0'), ('2/15/20', '0'), ('2/16/20', '0'), ('2/17/20', '0'), ('2/18/20', '0'), ('2/19/20', '0'), ('2/20/20', '0'), ('2/21/20', '0'), ('2/22/20', '0'), ('2/23/20', '0'), ('2/24/20', '0'), ('2/25/20', '0'), ('2/26/20', '0'), ('2/27/20', '0'), ('2/28/20', '0'), ('2/29/20', '0'), ('3/1/20', '1')])
#{'type': 'Feature', 'geometry': {'type': 'MultiPolygon', 'coordinates': [[[[19.80616760036355, 60.39630508483293], [19.8907508863511, 60.425109865684874], [20.12369537364009, 60.347362520130275], [20.2630558029241, 60.257194519274776], [20.244277952220898, 60.204917907909305], [20.054832458646672, 60.15561294576389], [20.048778533425434, 60.07913970899932], [20.17188835329665, 60.09400176896975], [20.231361389470692, 60.05547332815047], [20.13213920401097, 60.00266647223475], [19.937749860768974, 60.08988952709791], [19.743778228360327, 60.113414764066874], [19.69861030437886, 60.20100021637279], [19.89694404851673, 60.26686095891603], [19.80616760036355, 60.39630508483293]]], [[[19.633861544324304, 60.28019333169584], [19.679222105574013, 60.16838836463404], [19.547111513685365, 60.148803708558546], [19.543666840241258, 60.252334593160754], [19.633861544324304, 60.28019333169584]]]]}, 'properties': {'OBJECTID': 1, 'NAME': 'Åland', 'ISO3': 'ALA', 'ISO2': 'AX', 'FIPS': 'AX', 'COUNTRY': 'Åland', 'ENGLISH': 'Åland', 'FRENCH': '', 'SPANISH': '', 'LOCAL': 'Åland', 'FAO': '', 'WAS_ISO': '', 'SOVEREIGN': 'Finland', 'CONTINENT': 'Europe', 'UNREG1': 'Northern Europe', 'UNREG2': 'Europe', 'EU': 0, 'SQKM': 1243.71914338}}

json_file0={}
json_file0["type"]="FeatureCollection"
json_file0["features"]=[]

with open('ne_count14.json') as json_file:
    data = json.load(json_file)
    for elem in data["features"]:
         if elem["properties"]["iso"] not in ["US","CN","CA","KR","IR","NL"]:
              bb={}
              bb["type"]="Feature"
              bb["geometry"]={}
              bb["geometry"]["type"]=elem["geometry"]["type"]
              bb["geometry"]["coordinates"]=elem["geometry"]["coordinates"]
              bb["properties"]={}
              bb["properties"]["iso"]=elem["properties"]["iso"]
              bb["properties"]["name"]=elem["properties"]["name"]
              #bb["properties"]["woe_label"]=elem["properties"]["name"]
              bb["properties"]["code"]=elem["properties"]["code"]
              if elem["properties"]["name"] in list(all_data.keys()):
              #print(all_data[elem["properties"]["NAME_1"]]['2/29/20'])
              #bb["properties"]["min_zoom"]=all_data[elem["properties"]["NAME_1"]]['2/29/20']
                   bb["properties"]["scalerank"]=sum(all_data[elem["properties"]["name"]]['3/9/20'])
                   bb["properties"]["one_day"]=sum(all_data[elem["properties"]["name"]]['3/9/20'])-sum(all_data[elem["properties"]["name"]]['3/8/20'])
                   #print(bb["properties"]["name"],bb["properties"]["one_day"])
                   bb["properties"]["woe_label"]=dt_string
              else:
                   #bb["properties"]["min_zoom"]=0
                   bb["properties"]["scalerank"]=elem["properties"]["scalerank"]
                   #print(elem)
                   bb["properties"]["woe_label"]=elem["properties"]["woe_label"]
                   bb["properties"]["one_day"]=elem["properties"]["one_day"]
                   #print(bb["properties"]["one_day"])
                   #sum(all_data[elem["properties"]["name"]]['3/4/20'])-sum(all_data[elem["properties"]["name"]]['3/3/20'])
              json_file0["features"].append(bb)     
         else:
              json_file0["features"].append(elem)
#print(json_file0)          
with open('ne_count16.json', 'w') as outfile:
    json.dump(json_file0, outfile)            


