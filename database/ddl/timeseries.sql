create table timeseries (seriesname char(40), created datetime, value float);

create unique index i01_timeseries on timeseries(seriesname, created);

alter table timeseries modify column seriesname char(40);
