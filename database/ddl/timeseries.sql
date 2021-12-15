create table timeseries (seriesname char(30), created datetime, value float);

create unique index i01_timeseries on timeseries(seriesname, created);