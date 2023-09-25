# Multinational Retail Data Centralisation Project

## Table of Contents
- [Project Overview](#project-overview)
- [Extract and Clean the Data from the Data Sources](#extract-and-clean-the-data-from-the-data-sources)
- [Create the Database Schema](#create-the-database-schema)
- [Querying the Data](#querying-the-data)

## Project Overview
The multinational retail data centralisation project is a comprehensive data management and integration initiative designed to efficiently collect, process, and store diverse datasets from various sources. The primary goal of this project is to create a robust and organized data infrastructure, enabling informed decision-making and data-driven insights for a range of business needs.

## Extract and clean the data from the data sources 
In this section, we will discuss how I created the classes in order to extract data from various data sources, clean it, and store it in the `sales_data` database. Please find my scripts in the repository. 

Step 1: First, create a db_creds.yaml file containing the database credentials for the AWS RDS database

Step 2: Create a DatabaseConnector class, we will implement several essential methods to facilitate database interactions. Firstly, the read_db_creds method will be responsible for reading and retrieving database credentials stored in the db_creds.yaml file, returning them in dictionary form. Secondly, the init_db_engine method will be employed to establish and furnish an SQLAlchemy database engine using the extracted credentials. Additionally, we will utilize the list_db_tables method to compile a list of all available tables within the database, aiding in the identification of specific tables for data extraction. Lastly, we will design an upload_to_db method, enabling the seamless transfer of data from a Pandas DataFrame into the database.

Step 3: Create a DataExtractor class, implement the read_rds_table method. This function accepts a DatabaseConnector instance and a table name as parameters, extracting the specified table from the RDS database and returning it as a Pandas DataFrame.

Step 4: Create a DataCleaning class, create the clean_user_data method to handle data cleaning for user data obtained from the RDS database. This method addresses NULL values, date errors, data type discrepancies, and incorrect rows.

Step 5: Once the user data is extracted and cleaned, use the upload_to_db method to securely store the data in the sales_data database, placing it into a table named dim_users.

Step 6: For extracting data from PDFs, start by installing the tabula-py package. In the DataExtractor class, develop the retrieve_pdf_data method, which accepts a PDF document link as input and returns a Pandas DataFrame by utilizing the tabula-py package. In the DataCleaning class, create the clean_card_data method to clean card details extracted from the PDF. This process addresses erroneous values, NULL entries, and formatting issues.

Step 7: Create a DataExtractor class, create the list_number_of_stores method, which retrieves the count of stores to be extracted. This function requires the number of stores endpoint and a header dictionary with the API key. After determining the number of stores, implement the retrieve_stores_data method to extract store data from the API and store it in a Pandas DataFrame. In the DataCleaning class, design the clean_store_data method for cleaning the extracted store data.

Step 8: Begin by creating the extract_from_s3 method in the DataExtractor class. This function utilizes the boto3 package to download and extract product data from an S3 bucket, returning it as a Pandas DataFrame. Implement the convert_product_weights method in the DataCleaning class to standardize product weights to kilograms. Subsequently, create the clean_products_data method to address any erroneous values within the product data DataFrame.

Step 9: To extract order data from AWS RDS, start by listing all available tables using the previously created table listing methods. Next, utilize the read_rds_table method in the DataExtractor class to extract orders data, returning it as a Pandas DataFrame. Within the DataCleaning class, design the clean_orders_data method to refine the order data by removing unnecessary columns and ensuring proper formatting.

Step 10: The date and time data, stored in JSON format on S3, can be extracted and cleaned as follows: Create the retrieve_date_times_data method in the DataExtractor class to extract data from the JSON file, converting it into a Pandas DataFrame. In the DataCleaning class, implement the clean_date_times_data method to ensure the extracted date and time data is free of inconsistencies. Finally, upload the cleaned date and time data to the database, naming the table dim_date_times.


## Create the Database Schema
In this section I will discuss how I created the database schema as shown in my database_schema.sql file in this repository

In the process of creating our database schema, we're adjusting data types across various tables to align them with the desired formats. For the 'orders_table,' we're transitioning columns like 'date_uuid,' 'user_uuid,' 'card_number,' 'store_code,' 'product_code,' and 'product_quantity' to their appropriate data types. In the 'dim_user_table,' we're ensuring 'first_name' and 'last_name' become VARCHAR(255) and 'date_of_birth' converts to DATE. In the 'store_details_table,' we're merging duplicate latitude columns and altering data types accordingly. For the 'dim_products' table, we're cleansing the 'product_price,' 'weight,' 'EAN,' 'product_code,' 'date_added,' 'uuid,' 'still_available,' and introducing a 'weight_class' column. Adjusting data types extends to the 'dim_date_times' and 'dim_card_details' tables as well. Following this, primary keys are added to each 'dim' table, and foreign key constraints are established in the 'orders_table' to link these primary keys. This finalizes the creation of our star-based database schema, setting the stage for efficient data analysis.

## Querying the Data 
Now that all the previous steps have been completed create a querying_data.sql file which contains the queries you want to run to investigate the data. After running this querying_data.sql you should be able to see the answers to your investigations. The investigations I conducted are listed below:

How many stores does the business have and in which countries?
Which locations currently have the most stores?
Which months produce the average highest cost of sales typically?
How many sales are coming from online?
What percentage of sales come through each type of store?
Which month in each year produced the highest cost of sales?
What is our staff headcount?
Which German store type is selling the most?
How quickly is the company making sales?





