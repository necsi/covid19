import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
from os import path
from io import StringIO

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
        # @TODO: confirm whether second column and fourth column are sane guesses
        df = pd.DataFrame
        df=pd.read_csv(StringIO(raw_data),sep=";",names=["Municipality","GGD-region?","Count"],header=0,skiprows=3)

        #Process the reference date given in the comment section in the header
        comments={"Comments":[x.split(";")[0] for x in raw_data.split("\n")[2:4]]}

        dutch_months =["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
        trans_months = {month:number+1 for number, month in enumerate(dutch_months)}

        raw_reference_date=comments["Comments"][0].split(" ")[1:]
        print(raw_reference_date)
        day, month, hour = tuple(raw_reference_date)
        df["Reference date"] = f"{hour} {day}.{trans_months[month]}"

        year, day, month = (datetime.now().year,datetime.now().day, datetime.now().month)
        df["Fetch date"] =f"{day}.{month}.{year}"


        #Save file
        file_path = path.join(target_directory,"Netherlands_RIVM_data.csv")
        print(df)
        df.to_csv(file_path, index=False)
