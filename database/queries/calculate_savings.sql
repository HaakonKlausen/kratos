select da.pricedate, da.period, ts.value * da.pricenok / 1000 as SpotCost
  from timeseries ts, dayahead da 
 where ts.seriesname = 'oss.period_active_energy'
  and date(ts.created) = date(da.pricedate)
  and da.period = hour(ts.created)
  and da.pricedate between '2022-08-01' and '2022-08-31'
  order by da.pricedate, da.period;


# Spot Cost 

select sum(ts.value * da.pricenok / 1000) as SpotCost
  from timeseries ts, dayahead da 
 where ts.seriesname = 'oss.period_active_energy'
  and date(ts.created) = date(da.pricedate)
  and da.period = hour(ts.created)
  and da.pricedate between '2022-08-01' and '2022-08-31'
  order by da.pricedate, da.period;


# Mean spot price 
select avg(da.pricenok)
from dayahead da 
where da.pricedate between '2022-08-01' and '2022-08-31'

# Sum use
select sum(ts.value) / 1000 as value
from timeseries ts
 where ts.seriesname = 'oss.period_active_energy'
  and ts.created between '2022-08-01' and '2022-08-31';

August mean spot usage: 2349,84
Actual usage: 2245,92
Savings: = 103,92
Savings% = 4,42%

select (
select avg(da.pricenok)
from dayahead da 
where da.pricedate between '2022-08-01' and '2022-08-31'
) * 
(select sum(ts.value) / 1000 as value
from timeseries ts
 where ts.seriesname = 'oss.period_active_energy'
  and ts.created between '2022-08-01' and '2022-08-31') as MeanSpotCost;




select ((select sum(ts.value * (select avg(pricenok) from dayahead da where year(ts.created) = year(da.pricedate) and month(ts.created) = month(da.pricedate) ) / 1000) as value,
ts.created as time 
  from timeseries ts
 where ts.seriesname = 'oss.period_active_energy'
 and $__timeFilter(ts.created)) - 
(select sum(ts.value * da.pricenok / 1000) as value,
ts.created as time 
  from timeseries ts, dayahead da 
 where ts.seriesname = 'oss.period_active_energy'
  and date(ts.created) = date(da.pricedate)
  and da.period = hour(ts.created)
 and $__timeFilter(ts.created)))

