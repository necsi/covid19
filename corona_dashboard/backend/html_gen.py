import glob 
import os 
os.chdir('/Users/mac/Documents/GitHub/topojson/')
list_of_countries=sorted(glob.glob('/Users/mac/Documents/GitHub/topojson/countries/*/'))
str_html='<select id="countries">'




for fl in list_of_countries:
    files=sorted(glob.glob(fl+'*.json'))
    os.rename(files[0],'province_state.json')

    print(files)
    #print(files)
    #fl=fl.replace("./countries/","")[:-1]
    #fl=f'<option value="{fl}">{fl}</option>'
    #str_html=str_html+fl+'\n'
#str_html=str_html+'</select>'
#with open('html_code.html','w') as fl:
#    fl.write(str_html)