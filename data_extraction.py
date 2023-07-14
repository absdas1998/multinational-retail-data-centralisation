import sqlalchemy
import pandas as pd
import tabula
import requests
import awscliaws configure
import boto3

class DataExtractor:
    def read_rds_tables(self, engine, table_name):
        with engine.connect() as connection:
            query = sqlalchemy.text(f"SELECT * FROM {table_name}")
            result = connection.execute(query)
            data = pd.DataFrame(result.fetchall(), columns=result.keys())
            engine.dispose()
            return data
        
    def retrieve_pdf_data(self, link):
        tables = tabula.read_pdf(link, pages='all')
        dataframes = []
    
        for table in tables:
            dataframe = pd.DataFrame(table)
            dataframes.append(dataframe)
        
        result_df = pd.concat(dataframes, ignore_index=True)
        return result_df
    
    
    def list_number_of_stores(self, endpoint, headers):
        response = requests.get(endpoint, headers=headers)
        data = response.json()
        return data

    def retrieve_stores_data(self, endpoint, headers):
        df_list = []
        for store_number in range(0, 451):
            response = requests.get(endpoint.format(store_number), headers=headers)
            data = response.json()
            df_list.append(data) 
        df = pd.DataFrame(df_list)
        return df
        

        
    def extract_from_s3(self, s3_address):
        s3 = boto3.client('s3')
        address_without_prefix = s3_address.replace('s3://', '')
        bucket_name, file_key = address_without_prefix.split('/', 1)
        filename = file_key.split('/')[-1]
        s3.download_file(bucket_name, file_key, filename)
        if filename.endswith(".csv"):
            df = pd.read_csv(filename)
        elif filename.endswith(".json"):
            df = pd.read_json(filename)
        else:
            raise ValueError("Unsupported file format")
        return df
    


    
    
