import glob 
import os 
os.chdir('/Users/mac/Documents/GitHub/topojson/')
list_of_countries=sorted(glob.glob('/Users/mac/Documents/GitHub/topojson/countries/*/'))
str_html='<select id="countries">'




for fl in list_of_countries:
    
    files=sorted(glob.glob(fl+'*.json'))
    files_spl=files[0].split('/')
    s="/"
    s=s.join(files_spl[:-1])
    s=s+"/topo.json"
    os.rename(files[0],s)







    #
    #try:
    #    a=1
    #    #print(files[0])
    #except Exception as e:
    #    print(e)
    #os.rename(files[0],files[0]'province_state.json')

    #print(files)
    #fl=fl.replace("./countries/","")[:-1]
    #fl=f'<option value="{fl}">{fl}</option>'
    #str_html=str_html+fl+'\n'
#str_html=str_html+'</select>'
#with open('html_code.html','w') as fl:
#    fl.write(str_html)