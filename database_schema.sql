-- ALTER TABLE orders_table
-- ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID,
-- ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
-- ALTER COLUMN card_number TYPE VARCHAR(20),
-- ALTER COLUMN store_code TYPE VARCHAR(15),
-- ALTER COLUMN product_code TYPE VARCHAR(11),
-- ALTER COLUMN product_quantity TYPE SMALLINT;

-- ALTER TABLE dim_users
-- ALTER COLUMN first_name TYPE VARCHAR(255),
-- ALTER COLUMN last_name TYPE VARCHAR(255),
-- ALTER COLUMN date_of_birth TYPE DATE,
-- ALTER COLUMN country_code TYPE VARCHAR(2),
-- ALTER COLUMN user_uuid TYPE UUID USING user_uuid::UUID,
-- ALTER COLUMN join_date TYPE DATE;

-- ALTER TABLE dim_store_details
-- ADD COLUMN merged_latitude FLOAT;

-- UPDATE dim_store_details
-- SET merged_latitude = CASE
--     WHEN latitude = 'N/A' THEN NULL
--     ELSE latitude::FLOAT
-- END
-- WHERE latitude != 'N/A';

-- ALTER TABLE dim_store_details
-- DROP COLUMN latitude,
-- DROP COLUMN lat;

-- ALTER TABLE dim_store_details
-- RENAME COLUMN merged_latitude TO latitude;

-- UPDATE dim_store_details
-- SET longitude = NULL
-- WHERE longitude = 'N/A';

-- ALTER TABLE dim_store_details
-- ALTER COLUMN longitude TYPE double precision
-- USING longitude::double precision;

-- ALTER TABLE dim_store_details
-- ALTER COLUMN store_code TYPE VARCHAR(15);

-- ALTER TABLE dim_store_details
-- ALTER COLUMN staff_numbers TYPE SMALLINT
-- USING staff_numbers::SMALLINT;

-- ALTER TABLE dim_store_details
-- ALTER COLUMN opening_date TYPE DATE
-- USING opening_date::DATE;

-- ALTER TABLE dim_store_details
-- ALTER COLUMN store_type TYPE VARCHAR(225);

-- ALTER TABLE dim_store_details
-- ALTER COLUMN store_type DROP NOT NULL;

-- ALTER TABLE dim_store_details
-- ALTER COLUMN country_code TYPE VARCHAR(2);

-- ALTER TABLE dim_store_details
-- ALTER COLUMN continent TYPE VARCHAR(225);

-- UPDATE dim_store_details
-- SET locality = NULL
-- WHERE locality = 'N/A';

-- ALTER TABLE dim_store_details
-- ALTER COLUMN locality TYPE VARCHAR(255);

-- UPDATE dim_products
-- SET product_price = REPLACE(product_price, '£', ''); 

-- ALTER TABLE dim_products
-- ADD COLUMN weight_class VARCHAR(50);

-- UPDATE dim_products
-- SET weight_class = CASE
--     WHEN weight < 2 THEN 'Light'
--     WHEN weight >= 2 AND weight < 40 THEN 'Mid_Sized'
--     WHEN weight >= 40 AND weight < 140 THEN 'Heavy'
--     WHEN weight >= 140 THEN 'Truck_Required'
--     ELSE NULL -- Handle any other cases if necessary
-- END;

-- ALTER TABLE dim_products
-- ALTER COLUMN product_price TYPE FLOAT USING product_price::FLOAT;

-- ALTER TABLE dim_products
-- ALTER COLUMN weight TYPE FLOAT;

-- ALTER TABLE dim_products
-- ALTER COLUMN "EAN" TYPE VARCHAR(20);

-- ALTER TABLE dim_products
-- ALTER COLUMN product_code TYPE VARCHAR(11);

-- ALTER TABLE dim_products
-- ALTER COLUMN uuid TYPE UUID USING uuid::UUID;

-- ALTER TABLE dim_products
-- RENAME COLUMN removed TO still_avaliable;

-- UPDATE dim_products
-- SET still_avaliable = CASE
--     WHEN still_avaliable = 'Still_avaliable' THEN TRUE
--     WHEN still_avaliable = 'Removed' THEN FALSE
-- END;

-- ALTER TABLE dim_products
-- ALTER COLUMN still_avaliable TYPE BOOL USING still_avaliable::BOOL;

-- ALTER TABLE dim_products
-- ALTER COLUMN date_added TYPE DATE USING date_added::DATE;

-- ALTER TABLE dim_date_times
-- ALTER COLUMN month TYPE VARCHAR(2);

-- ALTER TABLE dim_date_times
-- ALTER COLUMN year TYPE VARCHAR(4);

-- ALTER TABLE dim_date_times
-- ALTER COLUMN day TYPE VARCHAR(2);

-- ALTER TABLE dim_date_times
-- ALTER COLUMN time_period TYPE VARCHAR(12);

-- ALTER TABLE dim_date_times
-- ALTER COLUMN date_uuid TYPE UUID USING date_uuid::UUID;

-- ALTER TABLE dim_card_details
-- ALTER COLUMN card_number TYPE VARCHAR(20);

-- ALTER TABLE dim_card_details
-- ALTER COLUMN expiry_date TYPE VARCHAR(5);

-- ALTER TABLE dim_card_details
-- ALTER COLUMN date_payment_confirmed TYPE DATE USING date_payment_confirmed::DATE;

-- ALTER TABLE dim_date_times
-- ADD PRIMARY KEY (date_uuid);

-- ALTER TABLE dim_users
-- ADD PRIMARY KEY (user_uuid);

-- ALTER TABLE dim_card_details
-- ADD PRIMARY KEY (card_number);

-- ALTER TABLE dim_store_details
-- ADD PRIMARY KEY (store_code);

-- ALTER TABLE dim_products
-- ADD PRIMARY KEY (product_code);

-- ALTER TABLE orders_table
-- ADD CONSTRAINT FK_orders_dim_date_times
-- FOREIGN KEY (date_uuid)
-- REFERENCES dim_date_times(date_uuid);

-- ALTER TABLE orders_table
-- ADD CONSTRAINT FK_orders_dim_users
-- FOREIGN KEY (user_uuid)
-- REFERENCES dim_users(user_uuid);

ALTER TABLE orders_table
ADD CONSTRAINT FK_orders_dim_card_details
FOREIGN KEY (card_number)
REFERENCES dim_card_details(card_number);

-- ALTER TABLE orders_table
-- ADD CONSTRAINT FK_orders_dim_store_details
-- FOREIGN KEY (store_code)
-- REFERENCES dim_store_details(store_code);

-- ALTER TABLE orders_table
-- ADD CONSTRAINT FK_orders_dim_products
-- FOREIGN KEY (product_code)
-- REFERENCES dim_products(product_code);


