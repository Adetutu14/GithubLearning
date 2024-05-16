create or replace table analytics.public.products as
select product_id, product_code,category, product_name, price
from sales_db.public.dim_product;