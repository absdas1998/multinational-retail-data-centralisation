
import yaml
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine, text
import psycopg2



class DatabaseConnector:
    def read_db_creds(self, creds_file):
        with open(creds_file, "r") as file:
            credentials = yaml.safe_load(file)
        return credentials
    
    def init_db_engine(self, creds):
        db_url = self.create_db_url(creds)
        engine = sqlalchemy.create_engine(db_url)
        return engine
    
    def create_db_url(self, creds):
        host = creds['RDS_HOST']
        port = creds['RDS_PORT']
        database = creds['RDS_DATABASE']
        username = creds['RDS_USER']
        password = creds['RDS_PASSWORD']
        db_url = f"postgresql://{username}:{password}@{host}:{port}/{database}"
        return db_url
    
    def list_db_tables(self, engine):
        with engine.connect() as connection:
            tables = connection.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public'"))
            table_names = [table[0] for table in tables]
            return table_names
    
    def __init__(self, host, port, database, user, password):
        ### Creates the parameters for uploading the database to the intended location ###
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password

    def upload_to_db(self, df, table_name):
        db_url = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        engine = sqlalchemy.create_engine(db_url)
        print(engine)
        with engine.connect() as connection:
            df.to_sql(table_name, engine, if_exists = "replace", index=False)
            
        engine.dispose()

        
# host = 'localhost'
# port = 5433
# database = 'sales_data'  
# username = 'postgres'
# password = 'Pw185253'
# connector = DatabaseConnector(host, port, database, username, password)
# read_creds = connector.read_db_creds("db_creds.yaml")
# init_db_engine = connector.init_db_engine(read_creds)
# list_tables = connector.list_db_tables(init_db_engine)
# print(list_tables)
# user_data = "legacy_users"
# extractor = DataExtractor()
# legacy_users_data = extractor.read_rds_tables(init_db_engine, user_data)

# user_cleaner = DataCleaning()
# clean_data = user_cleaner.clean_user_data(legacy_users_data)
# connector.upload_to_db(clean_data, "dim_users")    


        

       






    

    
    
