-- Database Name: etl_details
    -- Table Name #1: etl_status
    -- Table Name #2: etl_expected_time

-- View ETL Status Table
select * from etl_status; 


-- View ETL Expected Time Table
select * from etl_expected_time; 


-- Control ETL Status here

update etl_status
set last_success_date = CURRENT_DATE-1; -- ETL is delayed

update etl_status
set last_success_date = CURRENT_DATE-1; -- ETL is working fine


-- Control ETL Expected Time, incase of ETL Delay

update etl_expected_time
set expected_completion_time = '19:45:00';  -- Update Expected Time of Report Delivery
