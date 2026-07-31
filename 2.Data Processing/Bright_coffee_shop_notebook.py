# Databricks notebook source
--Checking full table
SELECT *
FROM bright.coffee.shop;

--Checking how many rows in the dataset and checking for duplicates
SELECT COUNT(*) AS num_of_rows,
       COUNT(DISTINCT transaction_id) AS user_id
FROM bright.coffee.shop;

--Checking for NULLS
SELECT COUNT(*) AS null_rows
FROM bright.coffee.shop
WHERE transaction_id IS NULL;

--Checking what is the starting date and the eding date of the dataset
SELECT MIN(transaction_date) AS earliest_date,
       MAX(transaction_date) AS latest_date
FROM bright.coffee.shop;

--Calculating Revenue while changing the unit_price from string to numeric data type for it to have dots instead of commas
SELECT SUM(transaction_qty * CAST(REPLACE(unit_price, ',', '.') AS DECIMAL(10,2))) AS total_amount 
FROM bright.coffee.shop;

--Adding total_amount on the table
ALTER TABLE bright.coffee.shop
ADD COLUMNS (total_amount DECIMAL(10,2));
UPDATE bright.coffee.shop
SET total_amount = ROUND(
    transaction_qty * CAST(REPLACE(unit_price, ',', '.') AS DECIMAL(10,2)),
    2
);

--Updating the column unit_price on the table
UPDATE bright.coffee.shop
SET unit_price = REPLACE(unit_price, ',', '.')
WHERE unit_price LIKE '%,%';

--Checking if the column has changed from having dots to commas
SELECT
    unit_price
FROM bright.coffee.shop
LIMIT 20;

--Checking how many branches are there
SELECT DISTINCT store_location,
               store_id
FROM bright.coffee.shop;

--Checking disctinct product category
SELECT DISTINCT product_category
FROM bright.coffee.shop;

--Checking disctinct product types
SELECT DISTINCT product_type
FROM bright.coffee.shop;

SELECT COUNT(DISTINCT product_type) AS product
FROM bright.coffee.shop
GROUP BY product_type;

--Checking the lowest and highest prices in unit_price
SELECT MIN(unit_price) AS lowest_unit_price,
       MAX(unit_price) AS highest_unit_price
FROM bright.coffee.shop;

--Checking the total revenue by store location 
SELECT DISTINCT store_location,
               SUM(transaction_qty * CAST(REPLACE(unit_price, ',', '.') AS DECIMAL(10,2))) AS total_amount
FROM bright.coffee.shop
GROUP BY store_location;

--Number of transactions
SELECT COUNT(DISTINCT transaction_id ) AS num_of_transactions
FROM bright.coffee.shop;

--Average number of transaction(on avarage a person spends this amount on a product)
SELECT ROUND(AVG(transaction_qty * CAST(REPLACE(unit_price, ',', '.') AS DECIMAL(10,2)))) AS average_transactions
FROM bright.coffee.shop;

--Checking the earliest and latest transaction time
SELECT
    MIN(transaction_time) AS earliest_time,
    MAX(transaction_time) AS latest_time
FROM bright.coffee.shop;

--Checking Revenue by product type
SELECT
    product_type,
    ROUND(SUM(total_amount),2) AS total_revenue
FROM bright.coffee.shop
GROUP BY product_type
ORDER BY total_revenue DESC;

--Checking revenue by product category
SELECT
    product_category,
    ROUND(SUM(total_amount),2) AS total_revenue
FROM bright.coffee.shop
GROUP BY product_category
ORDER BY total_revenue DESC;

--checking top 10 best selling products
SELECT
    product_detail,
    ROUND(SUM(total_amount),2) AS total_revenue
FROM bright.coffee.shop
GROUP BY product_detail
ORDER BY total_revenue DESC
LIMIT 10;

--what time of day performs best
SELECT
    transaction_time_bucket,
    ROUND(SUM(total_amount),2) AS revenue,
    SUM(transaction_qty) AS items_sold
FROM bright.coffee.shop
GROUP BY transaction_time_bucket
ORDER BY revenue DESC;

--checking revenue by month
SELECT
    MONTH(transaction_date) AS month_number,
    DATE_FORMAT(transaction_date,'MMMM') AS month,
    ROUND(SUM(total_amount),2) AS revenue
FROM bright.coffee.shop
GROUP BY
    MONTH(transaction_date),
    DATE_FORMAT(transaction_date,'MMMM')
ORDER BY month_number;

--checking revenue by day of week
SELECT
    DATE_FORMAT(transaction_date,'EEEE') AS day,
    ROUND(SUM(total_amount),2) AS revenue
FROM bright.coffee.shop
GROUP BY DATE_FORMAT(transaction_date,'EEEE');

-- checking Quantity sold by product category
SELECT
    product_category,
    SUM(transaction_qty) AS total_quantity
FROM bright.coffee.shop
GROUP BY product_category
ORDER BY total_quantity DESC;

--average order value
SELECT
ROUND(AVG(total_amount),2) AS average_order_value
FROM bright.coffee.shop;

--Creating a cleaned table
SELECT
    transaction_id,
    transaction_date,
    transaction_time,
    transaction_qty,
    store_id,
    store_location,
    product_id,
    CAST(REPLACE(unit_price, ',', '.') AS DECIMAL(10,2)) AS unit_price,
    total_amount,
    product_category,
    product_type,
    product_detail,
    --Adding Date Functions to the table
    DAYNAME(transaction_date) AS day_name,
    MONTHNAME(transaction_date) AS month_name,
    DAYOFWEEK(transaction_date) AS day_of_week,
    DATE_FORMAT(transaction_time,'HH:mm:ss') AS cleaned_time,
    HOUR(transaction_time) AS transaction_hour,

--Adding CASE statements to the table
--Time buckets
CASE
    WHEN HOUR(transaction_time) BETWEEN 6 AND 9 THEN 'Early Morning'
    WHEN HOUR(transaction_time) BETWEEN 10 AND 11 THEN 'Late Morning'
    WHEN HOUR(transaction_time) BETWEEN 12 AND 14 THEN 'Mid-day'
    WHEN HOUR(transaction_time) BETWEEN 15 AND 17 THEN 'Afternoon'
    WHEN HOUR(transaction_time) BETWEEN 18 AND 20 THEN 'Evening'
    ELSE 'Night'
END AS transaction_time_bucket,

--Day type bucket
CASE
    WHEN DAYOFWEEK(transaction_date) IN (1,7) THEN 'Weekend'
    ELSE 'Weekday'
END AS day_type,

--Promotion flag
CASE
    WHEN unit_price <AVG(unit_price) OVER()*0.90 THEN 'Promotion'
    ELSE 'Normal Price'
END AS promotionflag,
CASE
   WHEN total_amount >= 9 THEN 'High Sale'
   WHEN total_amount >= 5 THEN 'Medium Sale'
   ELSE 'Low Sale'
END AS sales_category
FROM bright.coffee.shop;

# COMMAND ----------

