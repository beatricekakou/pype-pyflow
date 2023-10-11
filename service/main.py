# importing the right libraries
import os
# panda reads datas from excel,csv,sql,mongo,etc.
import pandas as pd
# request ->  a python http library
import requests
# sqlalchemy -> a py library which helps devs working with sql;
# if you want to interact with mongo you have to use 'pymongo' instead of 'sqlalchemy'
# create_engine is a method from sqlalchemy which handles db connections
from sqlalchemy import create_engine
#now i can see my environment variables
from dotenv import load_dotenv

URL = "http://universities.hipolabs.com/search?country=France"


# extracting datas from a picked url
def extract(url: str) -> dict:
    data = requests.get(url).json()
    return data


# converting my extracted dictionary to a data frame ->
# (we can think of data frame like as csv with columns and rows and a lot of functionalities)
def transform(extracted_data: dict) -> pd.DataFrame:
    # transforming the dict in a data frame
    df = pd.DataFrame(extracted_data)

    # print("Number of universities from the api", len(df))
    filtered_df = df[df["name"].str.contains("Paris")]

    # print("Number of universities in Paris",len(df))
    filtered_df.loc[:, 'domains'] = filtered_df["domains"].apply(lambda x: ','.join(map(str, x)))
    filtered_df.loc[:, 'web_pages'] = filtered_df["web_pages"].apply(lambda x: ','.join(map(str, x)))
    filtered_df = filtered_df.reset_index(drop=True)
    return filtered_df[["domains", "country", "web_pages", "name"]]


def load(data_frame: pd.DataFrame) -> None:
    load_dotenv()
    # getting credentials from .env file
    db_host = os.getenv("POSTGRES_HOST")
    db_port = os.getenv("POSTGRES_PORT")
    db_usr = os.getenv("POSTGRES_USER")
    db_psw = os.getenv("POSTGRES_PSW")
    db_name = os.getenv("POSTGRES_DB")

    if None in [db_host, db_port, db_usr, db_psw, db_name]:
        raise EnvironmentError("Some or all database credentials are missing from the environment variables.")

    # loading data in a postgres db
    disk_engine = create_engine(f"postgresql://{db_usr}:{db_psw}@{db_host}:{db_port}/{db_name}")
    data_frame.to_sql('france_universities', disk_engine, if_exists='replace')
    print("done")


#running the script
my_data = extract(URL)
my_data_frame = transform(my_data)
load(my_data_frame)
