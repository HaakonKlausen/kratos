create table timeseries (seriesname char(40), created datetime, value float);

create unique index i01_timeseries on timeseries(seriesname, created);

alter table timeseries modify column seriesname char(40);

alter table timeseries add column updated datetime null;

create index i02_timeseries on timeseries(seriesname, updated)


create table timeseries_local (seriesname char(40), created datetime, value float);

create unique index i01_timeseries_local on timeseries_local(seriesname, created);
