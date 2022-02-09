SELECT
  date_add(d.pricedate, INTERVAL d.period hour) AS 'time',
    IF(
		(SELECT avg(ds.price * 10.12 / 1000)
		FROM dayahead ds
		WHERE DATE_FORMAT(date_add(ds.pricedate, INTERVAL ds.period hour), "%Y-%m" ) 
			= DATE_FORMAT(date_add(d.pricedate, INTERVAL d.period hour), "%Y-%m" ) 
		) > 0.7 and d.pricedate between '2021-12-01' and  '2022-04-01', 
			(((0.7 + (((d.price * 10.12 / 1000) - 0.7) / 2))
		+ 0.0345) * 1.25), (((d.price * 10.12 / 1000) + 0.0345) * 1.25))
	)  AS  'Rød-Grønn LOS pris inkl MVA'
FROM dayahead d
ORDER BY time


SELECT
  date_add(d.pricedate, INTERVAL d.period hour) AS 'time',
    IF(
		d.pricedate between '2021-12-01' and  '2022-04-01', 
			(((0.7 + (((d.price * 10.12 / 1000) - 0.7) / 2))
		+ 0.0345) * 1.25), (((d.price * 10.12 / 1000) + 0.0345) * 1.25))
	)  AS  'Rød-Grønn LOS pris inkl MVA'
FROM dayahead d
ORDER BY time


SELECT
  date_add(d.pricedate, INTERVAL d.period hour) AS 'time',
		(((0.7 + (((d.price * 10.12 / 1000) - 0.7) / 2))
		+ 0.0345) * 1.25)
	AS  'Rød-Grønn LOS pris inkl MVA'
FROM dayahead d
ORDER BY time



SELECT
  date_add(d.pricedate, INTERVAL d.period hour) AS 'time',
	IF((SELECT avg(ds.price * 10.12 / 1000)
		FROM dayahead ds
		WHERE DATE_FORMAT(date_add(ds.pricedate, INTERVAL ds.period hour), "%Y-%m" ) 
			= DATE_FORMAT(date_add(d.pricedate, INTERVAL d.period hour), "%Y-%m" ) 
		) > 0.7 and
		d.pricedate between '2021-12-01' and  '2022-04-01', 
		(((0.7 + (((d.price * 10.12 / 1000) - 0.7) / 2))
		+ 0.0345) * 1.25),
		((d.price * 10.12 / 1000) - 0.7))
	AS  'Rød-Grønn LOS pris inkl MVA'
FROM dayahead d
ORDER BY time

