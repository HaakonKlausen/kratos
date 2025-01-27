select min(value) min_temp
  from timeseries
 where seriesname='hytten.out.temp'
   and timestampdiff (HOUR, created, now()) < 48;

select created, timestampdiff (HOUR, created, now())
 from timeseries 
 where seriesname='hytten.out.temp'
