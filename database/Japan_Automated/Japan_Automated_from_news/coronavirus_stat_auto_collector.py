###### imports
import pandas as pd
import requests
url="https://docs.google.com/spreadsheets/d/1jfB4muWkzKTR0daklmf8D5F0Uf_IYAgcx_-Ij9McClQ/export?format=csv&id=1jfB4muWkzKTR0daklmf8D5F0Uf_IYAgcx_-Ij9McClQ&gid=0"

df=pd.read_csv(url)
last_date=df.sort_values(by="Date Announced",ascending=False).head(1)['Date Announced'].values[0]
df.to_csv(f'./japan_gender_location_{last_date}.csv')
df_grp=df.groupby(["Date Announced","Detected Prefecture"])['Detected Prefecture'].count()
df_final=pd.DataFrame(df_grp).unstack().fillna(0).cumsum()
df_final['Detected Prefecture']
df_final['Detected Prefecture'].to_csv(f'./japan_total_count_data_{last_date}.csv')