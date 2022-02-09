create table power_consumption (consumptiondate date, minute int, consumption decimal(10,2));

create unique index i01_power_consumption on power_consumption(consumptiondate, minute);