import os 
import zipfile
import pandas as pd 
from sqlalchemy import create_engine
import psycopg2

def extract(file_name :str,download_dir :str) -> None:
    """extracting csv file from kaggle"""
    try:
        path_zip_csv = os.path.join(download_dir,file_name+".zip")
        os.system(f"kaggle datasets download -d  hmavrodiev/sofia-air-quality-dataset -f {file_name} -p {download_dir} ")
        print(f"{file_name} has been downloaded")
        with zipfile.ZipFile(path_zip_csv,'r') as unzip_csv:
            unzip_csv.extractall(download_dir)
            print("Unzipped File")
    except FileNotFoundError as error:
        print(error)
        print("File Not Found")
    except FileExistsError as file_exist:
        print(file_exist)
        print("file already exist")

def turn_into_csv(file_path :str) -> pd.DataFrame:
    """turning csv file into dataframe"""
    try:
        df = pd.read_csv(file_path)
        print("DataFrame is Made")
        return df 
    except FileNotFoundError as file_error:
        print(file_error)
        print("File path does not exist")


def transform_data(df:str) -> pd.DataFrame:
    """transforming data dropping unamed column and converting column into datetime[ns] """
    try:
        df.drop(df.filter(regex="Unname"), axis=1, inplace=True)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.index.rename("measurement_id",inplace=True)
        df = df.round(decimals=3)
        df.index = df.index +1
        print("DataFrame Has Been Transformed")
        return df
    except AttributeError as error_attribute:
        print(error_attribute)
        print("Could Not Transform Data")

def ingest_data(df :str, user :str, password :str, host :str, port :str, db :str,table_name :str) -> None:
    """ingesting data to posgres local"""
    try:
        engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
        df.head(0).to_sql(name=table_name, con=engine, if_exists='replace')
        df.to_sql(name=table_name, con=engine,if_exists='append')
    except psycopg2.OperationalError as psycopg2_error:
        print(psycopg2_error)
        print("Unable to Ingest data")

def run_etl() -> None:
    """running the whole ETL process"""
    download_dir = "..\data"
    file_name = "2017-08_bme280sof.csv"
    extract(file_name,download_dir)
    file_path = "../data/2017-08_bme280sof.csv"
    raw_df = turn_into_csv(file_path)
    df = transform_data(raw_df)
    user = "root"
    password = "root"
    host = "localhost"
    port = "5432"
    db = "sofia_air_qty"
    table_name = "2017-08-air_qty"
    ingest_data(df,user,password,host,port,db,table_name)

    print("Each Task is Succesfully Completed")


if __name__=="__main__": 
    """running main"""
    run_etl() 
