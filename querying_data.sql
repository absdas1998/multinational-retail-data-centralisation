-- How many stores does the business have and in which countries?
SELECT country_code, COUNT(*) AS entry_count
FROM dim_store_details
WHERE country_code IN ('GB', 'US', 'DE')
GROUP BY country_code;

-- Which locations currently have the most stores?
SELECT locality, COUNT(*) AS entry_count
FROM dim_store_details
GROUP BY locality;

-- Which months produce the average highest cost os sales typically?
SELECT dd.month, SUM(ot.product_quantity * dp.product_price) AS total_sales
FROM dim_date_times dd
JOIN orders_table ot ON dd.date_uuid = ot.date_uuid
JOIN dim_products dp ON ot.product_code = dp.product_code
GROUP BY dd.month
ORDER BY total_sales DESC;

-- How many sales are coming from online?
SELECT
    CASE
        WHEN ot.store_code = 'WEB-1388012W' THEN 'Web'
        ELSE 'Offline'
    END AS store_type,
    COUNT(*) AS total_sales,
    SUM(ot.product_quantity) AS product_quantity_count
FROM orders_table ot
GROUP BY store_type;

-- What percentage of sales come through each type of store?
SELECT ds.store_type, SUM(ot.product_quantity * dp.product_price) AS total_sales, (SUM(ot.product_quantity * dp.product_price) / (SELECT SUM(ot2.product_quantity * dp2.product_price) FROM orders_table ot2 JOIN dim_products dp2 ON ot2.product_code = dp2.product_code)) * 100 AS percentage_of_total
FROM dim_store_details ds
JOIN orders_table ot ON ds.store_code = ot.store_code
JOIN dim_products dp ON ot.product_code = dp.product_code
GROUP BY ds.store_type;

-- Which month in each year produced the highest cost of sales?
SELECT total_sales, year, month
FROM (
       SELECT SUM(ot.product_quantity * dp.product_price) AS total_sales, dt.year, dt.month, ROW_NUMBER() OVER (PARTITION BY dt.year ORDER BY SUM(ot.product_quantity * dp.product_price) DESC) AS rn
    FROM dim_date_times dt
    JOIN orders_table ot ON dt.date_uuid = ot.date_uuid
    JOIN dim_products dp ON ot.product_code = dp.product_code
    GROUP BY dt.year, dt.month
) subquery
WHERE rn = 1
ORDER BY year;

-- What is our staff headcount?
SELECT country_code, SUM(staff_numbers) AS total_staff_count
FROM dim_store_details
GROUP BY country_code;

-- Which German store type is selling the most?
SELECT  ds.country_code, ds.store_type, SUM(ot.product_quantity * dp.product_price) AS total_sales
FROM dim_store_details ds
JOIN orders_table ot ON ds.store_code = ot.store_code
JOIN dim_products dp ON ot.product_code = dp.product_code
WHERE ds.country_code = 'DE'
GROUP BY ds.country_code, ds.store_type;

-- How quickly is the company making sales?

WITH sales AS (
  SELECT
    timestamp,
    CONCAT(year, '-', month, '-', day) AS sale_datetime
  FROM dim_date_times
),

time_diff AS (
  SELECT
    sale_datetime::timestamp,
    LEAD(sale_datetime::timestamp) OVER (ORDER BY sale_datetime::timestamp) AS next_sale_datetime,
    LEAD(sale_datetime::timestamp) OVER (ORDER BY sale_datetime::timestamp) - sale_datetime::timestamp AS time_difference
  FROM sales
),

average_time_diff AS (
  SELECT
    EXTRACT(YEAR FROM sale_datetime::timestamp) AS year,
    AVG(EXTRACT(EPOCH FROM time_difference)) AS avg_time_taken
  FROM time_diff
  GROUP BY year
)

SELECT
  year,
  TO_CHAR(INTERVAL '1 second' * avg_time_taken, '"hours": HH, "minutes": MI, "seconds": SS, "milliseconds": 0') AS actual_time_taken
FROM average_time_diff;











































