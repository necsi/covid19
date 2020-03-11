import pandas as pd
import json
### get data from BarishNews telegram news server. It is daily number
str_barishnews="{"+""""◽️تهران: 256
◽️قم: 53
◽️گیلان: 5
◽️اصفهان: 170
◽️البرز: 45
◽️مازندران: 32
◽️مرکزی: 31
◽️قزوین: 27
◽️سمنان: 63
◽️گلستان: 9
◽️خراسان رضوی: 34
◽️فارس: 19
◽️لرستان: 9
◽️آذربایجان شرقی: 29
◽️خوزستان: 17
◽️یزد: 23
◽️زنجان: 22
◽️کردستان: 6
◽️اردبیل: 1
◽️کرمانشاه: 8
◽️کرمان: 18
◽️همدان: 7
◽️سیستان و بلوچستان: 4
◽️هرمزگان: 10
◽️خراسان جنوبی: 15
◽️خراسان شمالی: 11
◽️چهارمحال و بختیاری: 1
◽️ایلام: 6
◾️آذربایجان غربی: 27
◽️کهگیلویه و بویراحمد: 0
◽️بوشهر: 0
""".replace("◽️",",").replace("◾️",",").replace("مورد","")\
.replace("تهران","'Tehran'")\
.replace("اصفهان","'Esfahan'")\
.replace("قم","'Qom'")\
.replace("مازندران","'Mazandaran'")\
.replace("گیلان","'Gilan'")\
.replace("مرکزی","'Markazi'")\
.replace("سمنان","'Semnan'")\
.replace("قزوین","'Qazvin'")\
.replace("گلستان","'Golestan'")\
.replace("البرز","'Alborz'")\
.replace("لرستان","'Lorestan'")\
.replace("آذربایجان شرقی","'East Azarbaijan'")\
.replace("فارس","'Fars'")\
.replace("یزد","'Yazd'")\
.replace("خوزستان","'Khuzestan'")\
.replace("خراسان رضوی","'Khorasan-e-Razavi'")\
.replace("خراسان شمالی","'Northern Khorasan'")\
.replace("زنجان","'Zanjan'")\
.replace("خراسان جنوبی","'South Khorasan'")\
.replace("اردبیل","'Ardebil'")\
.replace("کردستان","'Kordestan'")\
.replace("همدان","'Hamedan'")\
.replace("آذربایجان غربی","'West Azarbaijan'")\
.replace("هرمزگان","'Hormozgan'")\
.replace("ایلام","'Ilam'")\
.replace("کرمانشاه","'Kermanshah'")\
.replace("کرمان","'Kerman'")\
.replace("سیستان و بلوچستان","'Sistan and Baluchestan'")\
.replace("چهارمحال و بختیاری","'Chahar mahall and Bakhitari'")\
.replace("کهگیلویه و بویراحمد","'Kohgiluyeh and BuyerAhmad'")\
.replace("بوشهر","'Bushehr'")[2:]+"}"
dict_barishnews=eval(str_barishnews)
df_iran=pd.DataFrame.from_dict(dict_barishnews,orient='index',columns=['Number_of_Cases'])
df_iran=df_iran.sort_values(by='Number_of_Cases',ascending='Fasle')
df_iran.to_csv('iran_daily.csv')
print(df_iran)