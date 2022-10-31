import datetime
import os
import pytz
import time

import constants
from configobj import ConfigObj
from pathlib import Path 
import mysql.connector
import kratoslib

class kratosdb():

	def __init__(self):
		self.__config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
		self.__connection = self.get_connection()


	def get_connection(self):
		try:
			connection = mysql.connector.connect(user=self.__config['user'], password=self.__config['password'],
									host=self.__config['host'],
									database=self.__config['database'])
			return connection
		except Exception as e:
			print('Error: ' + str(e))
			kratoslib.writeKratosLog('ERROR', 'Error in getting connection: ' + str(e))
		return


	def close_connection(self):
		self.__connection.close()


	def get_cursor(self):
		succeeded = True
		try:
			cursor = self.__connection.cursor()
		except:
			Succeeded = False
			kratoslib.writeKratosLog('ERROR', 'Error in getting cursor, retrying: ' + str(e))

		if not succeeded:
			succeeded = True
			try:
				self.__connection = self.get_connection()
				cursor = self.__connection.cursor()
			except:
				succeeded = False
				kratoslib.writeKratosLog('ERROR', 'Error in getting cursor, giving up: ' + str(e))
		
		if succeeded:
			return cursor
		else:
			return
		

	def writeKratosDataToSql(self, dataname, value):
		sql = ("select count(*) cnt from kratosdata where dataname=%(dataname)s")
		data = (dataname)
		count = 0
		cursor=self.get_cursor()
		cursor.execute(sql, { 'dataname': dataname })
		for cnt in cursor:
			count = cnt[0]
		cursor.close()
		if count == 1:
			sql = ("UPDATE kratosdata set value=%s where dataname=%s")
			data=(value, dataname)
			cursor=self.get_cursor()
			cursor.execute(sql, data)
		else:
			sql = ("INSERT INTO kratosdata(dataname, value) values (%s, %s)")
			data=(dataname, value)
			cursor=self.get_cursor()
			cursor.execute(sql, data)

		cursor.commit()
		cursor.close()


	def readKratosDataFromSql(self, dataname):
		sql = ("select value from kratosdata where dataname=%(dataname)s")
		retval = ''
		cursor=self.get_cursor()
		cursor.execute(sql, { 'dataname': dataname })
		for val in cursor:
			retval = val[0]
		cursor.close()
		return retval


	def writeTimeseriesData(self, seriesname, value):
		now=datetime.datetime.now()
		self.writeTimeseriesDataTime(seriesname, value, now)


	def writeTimeseriesDataTime(self, seriesname, value, now):
		sql = ("INSERT INTO timeseries_local (seriesname, created, value) "
				"VALUES (%s, %s, %s)")
		try:	
			cursor=self.get_cursor()
			data = (seriesname, now, value)
			cursor.execute(sql, data)
			cursor.commit()
			cursor.close()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in storing timeseries ' + seriesname + ': ' + str(value) + ' (' + str(e) + ')')
		# Write current value of log as key/value data
		self.writeKratosData(seriesname, str(value))


	def readLastTwoTimeseriesData(self, seriesname):
		sql = ("select value from timeseries where seriesname=%(seriesname)s order by created desc limit 2")
		lastvalue=0
		priorvalue=0
		cursor=self.get_cursor()
		cursor.execute(sql, { 'seriesname': seriesname })
		row=0
		for value in cursor:
			if row==0:
				lastvalue=value[0]
			if row==1:
				priorvalue=value[0]
			row=row+1
		cursor.close()
		return lastvalue, priorvalue


	def getMinimumTimeSeriesValue(self, seriesname, numberOfHours):
		sql = ("select min(value) minvalue from timeseries where seriesname=%(seriesname)s and timestampdiff (HOUR, created, now()) < %(numberOfHours)s;")
		cursor=self.get_cursor()
		cursor.execute(sql, { 'seriesname': seriesname, 'numberOfHours': numberOfHours })
		retval = constants.EOL
		for minvalue in cursor:
			retval = minvalue[0]
			break
		return retval



	def writeStatuslogData(self, logname, value):
		now=datetime.datetime.now()
		self.writeStatuslogDataTime(logname, value, now)


	def getLatestStatuslog(self, logname):
		sql = ("select value, created from statuslog_local where logname=%(logname)s order by created desc limit 1")
		retval_value = ''
		retval_created = ''
		cursor=self.get_cursor()
		cursor.execute(sql, { 'logname': logname })
		for value, created in cursor:
			retval_value = value
			retval_created = created
		cursor.close()
		return retval_value, retval_created
		pass		


	def writeStatuslogDataTime(self, logname, value, now):
		oldvalue, oldcreated = self.getLatestStatuslog(logname)
		# Insert only if value has changed, otherwise keep last status
		if value != oldvalue:
			self.insertStatuslogDataTime(logname, value, now)


	def insertStatuslogDataTime(self, logname, value, now):
		sql = ("INSERT INTO statuslog_local (logname, created, value) "
				"VALUES (%s, %s, %s)")
		try:	
			cursor=self.get_cursor()
			data = (logname, now, value)
			cursor.execute(sql, data)
			cursor.commit()
			cursor.close()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in inserting statuslog ' + logname + ': ' + str(value) + ' (' + str(e) + ')')
		# Write current value of log as key/value data
		self.writeKratosDataToSql(logname, str(value))


	def updateCreatedStatuslogDataTime(self, logname, created, now):
		sql = ("UPDATE statuslog_local SET created=%s where logname=%s and created=%s")
		try:	
			cursor=self.get_cursor()
			data = (now, logname, created)
			cursor.execute(sql, data)
			cursor.commit()
			cursor.close()
		except Exception as e:
			kratoslib.writeKratosLog('ERROR', 'Error in updating statuslog creation time ' + logname + ': ' + str(created) + ' (' + str(e) + ')')

if __name__ == "__main__":
	db = kratosdb()
	print(db.getMinimumTimeSeriesValue('hytten.out.temp', 48))