import datetime
import time 

import kratoslib
import kratosdb

import constants

def getSeriesnames():
    sql = ("select distinct seriesname from timeseries")
    connection=kratoslib.getConnection()
    cursor=connection.cursor()
    cursor.execute(sql)
    seriesNames=[]
    for value in cursor:
        seriesNames.append(value[0])
    cursor.close()	
    connection.close()
    return seriesNames
		

def getFirstDate(seriesname):
    sql = ("select date(created) + interval 1 day from timeseries where seriesname=%(seriesname)s order by created asc limit 1")    
    connection=kratoslib.getConnection()
    cursor=connection.cursor()
    cursor.execute(sql, { 'seriesname': seriesname })
    firstDate=None
    for value in cursor:
        firstDate=value[0]
    cursor.close()
    connection.close()
    return firstDate

def listData(seriesname, firstdate):
    sql = f"select seriesname, created, value, updated from timeseries where seriesname = '{seriesname}' and created < '{firstdate}' "
    connection=kratoslib.getConnection()
    cursor=connection.cursor()
    cursor.execute(sql)
    for row in cursor:
        created=row[1]
        value=row[2]
        updated=row[3]
        print(f"{created}: {value} {updated}")
        insertArchiveRow(connection=connection, seriesname=seriesname, created=created, value=value, updated=updated)

def insertArchiveRow(connection, seriesname, created, value, updated):
    if updated is None:
        sql = f"insert into timeseries_archive (seriesname, created, value) values ('{seriesname}', '{created}', {value})"
    else:
        sql = f"insert into timeseries_archive (seriesname, created, value, updated) values ('{seriesname}', '{created}', {value}, '{updated}')"
    cursor=connection.cursor()
    cursor.execute(sql)
    cursor.close()

def populateArchive(seriesname, firstdate):
    sql = f"insert into timeseries_archive(seriesname, created, value, updated) select seriesname, created, value, updated from timeseries where seriesname = '{seriesname}' and created < '{firstdate}' "
    connection=kratoslib.getConnection()
    cursor=connection.cursor()
    cursor.execute(sql)
    cursor.close()
    connection.close()

seriesNames = getSeriesnames()
for seriesName in seriesNames:
    firstdate = getFirstDate(seriesName)
    print(f"{seriesName}: {firstdate}")
    populateArchive(seriesname=seriesName, firstdate=firstdate)
    #listData(seriesname=seriesName, firstdate=firstdate)