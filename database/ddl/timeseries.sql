create table timeseries (seriesname char(40), created datetime, value float);

create unique index i01_timeseries on timeseries(seriesname, created);

alter table timeseries modify column seriesname char(40);

alter table timeseries add column updated datetime null;

create index i02_timeseries on timeseries(seriesname, updated)


create table timeseries_local (seriesname char(40), created datetime, value float);

create unique index i01_timeseries_local on timeseries_local(seriesname, created);

create index i03_timeseries on timeseries(created);

create table timeseries_archive (seriesname char(40), created datetime, value float, updated datetime null);

create unique index i01_timeseries_archive on timeseries_archive(seriesname, created);

create index i03_timeseries_archive on timeseries_archive(created);



select count(*) from timeseries where created < '2020-01-01T00:00:00';

insert into timeseries_archive(seriesname, created, value, updated) select seriesname, created, value, updated from timeseries where seriesname='yr.wind_speed' and created < '2021-12-16'

delete from timeseries where created <  '2020-01-01T00:00:00';