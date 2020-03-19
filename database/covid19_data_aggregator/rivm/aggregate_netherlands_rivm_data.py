import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from os import path
from io import StringIO
import re

def download_netherlands_rivm_data(target_directory):
        """
        Download the Netherlands Rijksinstituut voor Volksgezondheid
        en Milieu data

        :param target_directory: str
        :return None
        """

        #The url of the Rijksinstituut data
        rivm_url ="https://www.rivm.nl/coronavirus-kaart-van-nederland#node-coronavirus-covid-19-meldingen"

        #Fetch the data
        response = requests.get(rivm_url)
        soup =BeautifulSoup(response.text,"html.parser")
        raw_data = soup.find_all("div",id="csvData")[0].string

        raw_data_rows = [r for r in raw_data.split("\n") if r!=""]
        # @TODO: confirm whether second column and fourth column are sane guesses
        #List columns
        columns =raw_data_rows[0].split(";")


        #Parse out the comment rows indicated by rows starting with negative integers
        exp ="-\d+;"
        comments = {x:y for x,y in enumerate(raw_data_rows[1:]) if re.match(exp,y) }
        #clean the negative integer out.
        comments={x:re.sub(exp,"",y) for x,y in comments.items()}

        #Select the data rows: all rows except header row and comment rows
        data_idx =1+len(comments)
        data =raw_data_rows[data_idx:]

        df=pd.read_csv(StringIO("\n".join(data)),sep=";",names=columns,header=0,skiprows=data_idx)

        year, day, month = (datetime.now().year,datetime.now().day, datetime.now().month)
        df["Fetch date"] =f"{day}.{month}.{year}"
        df["Comments"] = "\n".join(list(comments.values()))


        #Save file
        file_path = path.join(target_directory,"Netherlands_RIVM_data.csv")
        print(df)
        df.to_csv(file_path, index=False)
