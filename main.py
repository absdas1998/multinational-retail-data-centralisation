
import yaml
import sqlalchemy
import pandas as pd
import tabula
import requests
import boto3
import awscli
from dateutil.parser import parse
from sqlalchemy import create_engine, text
from data_extraction import DataExtractor
from data_cleaning import DataCleaning
from database_utils import DatabaseConnector

host = 'localhost'
port = 5433
database = 'sales_data'  
username = 'postgres'
password = 'Pw185253'
connector = DatabaseConnector(host, port, database, username, password)
read_creds = connector.read_db_creds("db_creds.yaml")
init_db_engine = connector.init_db_engine(read_creds)
list_tables = connector.list_db_tables(init_db_engine)
user_data = "legacy_users"
extractor = DataExtractor()
legacy_users_data = extractor.read_rds_tables(init_db_engine, user_data)

cleaner = DataCleaning()
clean_data = cleaner.clean_user_data(legacy_users_data)
connector.upload_to_db(clean_data, "dim_users")
credit_card_data = extractor.retrieve_pdf_data("https://data-handling-public.s3.eu-west-1.amazonaws.com/card_details.pdf")



clean_credit_card_data = cleaner.clean_card_data(credit_card_data)
connector.upload_to_db(clean_credit_card_data, "dim_card_details")
# extractor = DataExtractor()
# cleaner = DataCleaning()

# header = {
#     "x-api-key": "yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX"
# }
# number_of_stores = extractor.list_number_of_stores("https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/number_stores", header)


# endpoint = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/store_details/{}"
# all_stores_data = extractor.retrieve_stores_data(endpoint, header)
# clean_all_stores_data = cleaner.clean_store_data(all_stores_data)
# clean_all_stores_data.to_csv("clean_all_stores_data.csv", index=False)
# connector.upload_to_db(clean_all_stores_data, "dim_store_details")



# product_weights_data = extractor.extract_from_s3("s3://data-handling-public/products.csv")
# converted_product_weight_data = cleaner.covert_product_weights(product_weights_data)
# cleaned_product_data = cleaner.clean_products_data(converted_product_weight_data)
# connector.upload_to_db(cleaned_product_data, "dim_products")

orders_data = "orders_table"
orders_table = extractor.read_rds_tables(init_db_engine, orders_data)
clean_orders_table = cleaner.clean_orders_data(orders_table)
connector.upload_to_db(clean_orders_table, "orders_table")

# date_details = pd.read_json("date_details.json")
# clean_date_details = cleaner.clean_date_details(date_details)
# connector.upload_to_db(clean_date_details,"dim_date_times")













