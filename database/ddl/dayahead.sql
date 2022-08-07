create table dayahead (pricearea char(3), pricedate date, period int, price decimal(10,2));

create unique index i01_dayahead on dayahead(pricearea, pricedate, period);

grant select, insert, update, delete on kratosdb.* to 'kratos_writer'@'localhost';

grant select on kratosdb.* to 'kratos_reader'@'localhost';

alter table dayahead add pricenok decimal(10,2);