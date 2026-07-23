CREATE or replace() DATABASE SMOOTHIES;

create or replace table smoothies.public.orders (
       order_uid integer default smoothies.public.order_seq.nextval,
       order_filled boolean default false,
       name_on_order varchar(100),
       ingredients varchar(200),
       constraint order_uid unique (order_uid),
       order_ts timestamp_ltz default current_timestamp()
);

create or replace file format smoothies.public.two_headerrow_pct_delim
  type = CSV,
  skip_header = 2,
  field_delimiter = '%',
  trim_space = TRUE
;


SELECT $1, $2, $3, $4, $5
FROM @SMOOTHIES.PUBLIC.MY_UPLOAD_FILES/fruits_available_for_smoothies.txt
(FILE_FORMAT => smoothies.public.two_headerrow_pct_delim);


COPY INTO smoothies.public.fruit_options (FRUIT_ID, FRUIT_NAME)
FROM (SELECT $2, $1 FROM @SMOOTHIES.PUBLIC.MY_UPLOAD_FILES/fruits_available_for_smoothies.txt)
FILE_FORMAT = (FORMAT_NAME = smoothies.public.two_headerrow_pct_delim)
ON_ERROR = ABORT_STATEMENT;


ALTER TABLE SMOOTHIES.PUBLIC.ORDERS
ADD ORDER_FILLED boolean default FALSE;

update smoothies.public.orders
set order_filled = true
where name_on_order is null;



alter table SMOOTHIES.PUBLIaC.ORDERS 
modify column order_uid 
default smoothies.public.order_seq.nextval;


CREATE FUNCTION util_db.public.SUM_MYSTERY_BAG_VAR(VAR1 NUMBER, VAR2 NUMBER, VAR3 NUMBER)
    RETURNS NUMBER AS 'SELECT VAR1+VAR2+VAR3';

SELECT util_db.public.SUM_MYSTERY_BAG_VAR(-10.5,2,1000);



CREATE OR REPLACE FUNCTION UTIL_DB.PUBLIC.NEUTRALIZE_WHINING(VAR4 TEXT)
    RETURNS TEXT AS 'SELECT INITCAP(VAR4)';


UPDATE SMOOTHIES.PUBLIC.FRUIT_OPTIONS
SET SEARCH_ON='Ugli Fruit (Jamaican Tangelo)' where FRUIT_NAME='Ugli Fruit';

select fruit_name, search_on from fruit_options;



select * from orders;
truncate orders;
