create table telldusdevice(deviceid char(7), devicename char(30), rom char(30), currentstate char(3), desiredstate char(3), desiredvalue int, commands int);

create unique index i01_telldusdevice on telldusdevice(deviceid);

create unique index i02_telldusdevice on telldusdevice(devicename);

create index i03_telldusdevice on telldusdevice(rom);