#impoting the right libraries

#panda reads datas from excel,csv,sql,mongo,etc.
import pandas as pd
#request ->  a python http library
import requests
#sqlalchemy -> a py library which helps devs working with sql; if you want to interact with mongo you have to use 'pymongo' insted of 'sqlalchemy'
#create_engine is a method from sqlalchemy which handles db connections
from sqlalchemy import create_engine

URL = "http://universities.hipolabs.com/search?country=France"

#extracting datas from a picked url
def extract(url:str) -> dict:
    datas = requests.get(url).json()
    return datas

#converting my extracted dictionary to a data frame (we can think of data frame like as csv with columns and rows and a lot of functionalities)
def transform(data:dict) -> pd.DataFrame:
    #trasforming the dict in a data frame
    df = pd.DataFrame(data)
    #print("Number of universities from the api", len(df))
    df = df[df["name"].str.contains("Paris")]
    df['domains'] = [','.join(map(str,l)) for l in df["domains"]]
    print(df["domains"])
    df['web_pages'] = [','.join(map(str, l)) for l in df["web_pages"]]
    #print("Number of universities in Paris",len(df))
    df = df.reset_index(drop=True)
    return df[["domains","country","web_pages","name"]]


def load(df:pd.DataFrame) -> None:
    #loads data in a postgres db
    disk_engine= create_engine("postgresql://postgres:postgres@localhost:5433/pipepyflow_db")
    df.to_sql('france_universities',disk_engine,if_exists='replace')
    print("done")

data = extract(URL)
df = transform(data)
#load(df)