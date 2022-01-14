create table statuslog (logname char(30), created datetime, value varchar(250));

create unique index i01_statuslog on statuslog(logname, created);