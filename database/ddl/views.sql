create or replace view in_temp_60min_avg as
select created, ROUND( ( select sum(t2.value) / count(t2.value)
from timeseries as t2
where t2.seriesname = t1.seriesname and timestampdiff (MINUTE, t2.created, t1.created) < 60), 1) as '60min_avg'
from timeseries as t1
where t1.seriesname = 'in.temp';