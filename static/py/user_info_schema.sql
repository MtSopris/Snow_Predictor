drop table if exists user_info;

create table user_info (
	utc_now varchar,
	input_date varchar,
	zip_code varchar, 
	dream varchar,
	planned varchar, 
	activity varchar
);

select * from user_info;

drop table if exists user_info_2;

create table user_info_2 (
	utc_now timestamp, 
	input_date DATE,
	zip_code varchar
);

select * from user_info_2;