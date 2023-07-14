import pandas as pd
import re
import yaml
import sqlalchemy
import psycopg2
from sqlalchemy import create_engine
from dateutil.parser import parse


class DataCleaning:
    
    @staticmethod
    def _is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return email if re.match(pattern, email) else None
    
    

    def clean_user_data(self, df):

        
        df["join_date"] = pd.to_datetime(df["join_date"], errors="coerce")
        df["date_of_birth"] = pd.to_datetime(df["date_of_birth"], errors="coerce")

       
        df['first_name'] = df['first_name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
        df['last_name'] = df['last_name'].str.replace(r'[^a-zA-Z\s]', '', regex=True)
        df["first_name"] = df["first_name"].str.capitalize()
        df["last_name"] = df["last_name"].str.capitalize()

        
        df['email_address'] = df['email_address'].apply(self._is_valid_email)

        
        valid_countries = ["Germany", "United Kingdom", "United States"]
        df.loc[~df['country'].isin(valid_countries), 'country'] = None

        valid_country_codes = ["DE", "GB", "US"]
        df.loc[~df['country_code'].isin(valid_country_codes), 'country_code'] = None

        
        df.dropna(inplace=True)

        return df


    def clean_card_data(self, df):
        df['date_payment_confirmed'] = pd.to_datetime(df['date_payment_confirmed'], errors='coerce').dt.date
        df = df.dropna()
        df.loc[:, 'card_number'] = df['card_number'].apply(lambda x: re.sub(r'\?', '', str(x)))
        return df
        
    
    def covert_product_weights(self, df):
       def convert_to_kg(weight):
            weight = str(weight).lower()
            if 'kg' in weight:
                weight = re.sub(r'[^\d.]+', '', str(weight))
                weight = float(weight)
            elif 'x' in weight:
                parts = weight.split('x')
                if len(parts) != 2:
                    return weight  # Unexpected format, return weight as is
                quantity = float(parts[0])
                value = float(re.sub(r'\D', '', parts[1]))
                value = value / 1000
                weight = quantity * value
            elif 'g' in weight:
                weight = re.sub(r'\D', '', weight)  # Remove non-numeric characters
                weight = float(weight) / 1000.0  # Convert grams to kilograms
            elif 'ml' in weight:
                weight = re.sub(r'\D', '', weight)  # Remove non-numeric characters
                weight = float(weight) / 1000.0  # Convert milliliters to kilograms
            elif 'oz' in weight:
                weight = re.sub(r'\D', '', weight)  # Remove non-numeric characters
                weight = float(weight) * 0.0283495  # Convert ounces to kilograms
            else:
                weight = None  # Handle unexpected format gracefully, set weight to None
            return weight
       

       df["weight"] = df['weight'].apply(convert_to_kg)
       return df
    


    def clean_products_data(self, df):
        df["uuid"] = df["uuid"].apply(self._check_user_uuid)
        df = df[~df['removed'].str.contains(r'\d', na=False)]
        df = df.dropna()
        df = df.drop_duplicates()
        df['date_added'] = df['date_added'].apply(lambda x: parse(x).strftime('%Y-%m-%d') if isinstance(x, str) else x)
        return df
        
    
    def clean_orders_data(self, df):
        columns_to_remove = ['first_name', 'last_name', '1']
        df = df.drop(columns_to_remove, axis=1)
        return df

    def clean_store_data(self, df):
        df = df.drop(df[df['country_code'].str.len() > 2].index)
        df['continent'] = df['continent'].replace('ee', '', regex=True)
        df['staff_numbers'] = df['staff_numbers'].str.replace(r'\D', '', regex=True)
        mask = df['opening_date'].str.match(r'^[a-zA-Z]+ \d{4} \d{2}$')
        df.loc[mask, 'opening_date'] = pd.to_datetime(df.loc[mask, 'opening_date'], format='%B %Y %d').dt.strftime('%Y-%m-%d')
        df['opening_date'] = df['opening_date'].apply(lambda x: parse(str(x)).strftime('%Y-%m-%d') if not pd.isnull(x) else x)
        return df
    


    def clean_date_details(self, df):
        df['month'] = pd.to_numeric(df['month'], errors='coerce')
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
        df['day'] = pd.to_numeric(df['day'], errors='coerce')
        df = df.dropna(subset=['month', 'year', 'day'])
        df = df.dropna()
        return df

        


        






