import glob 

list_of_countries=sorted(glob.glob("./countries/*/"))
str_html='<select id="countries">'


for fl in list_of_countries:
    fl=fl.replace("./countries/","")[:-1]
    fl=f'<option value="{fl}">{fl}</option>'
    str_html=str_html+fl+'\n'
str_html=str_html+'</select>'
with open('html_code.html','w') as fl:
    fl.write(str_html)