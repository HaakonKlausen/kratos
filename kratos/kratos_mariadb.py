import kratoslib
import mariadb 

class kratos_mariadb():
    def __init__(self):
        self.__config = ConfigObj(kratoslib.getKratosConfigFilePath('kratosdb.conf'))
        self.__connection = self.get_connection()


    def get_connection(self):
        try:
            connection = mariadb.connect(user=self.__config['user'], password=self.__config['password'],
                                    host=self.__config['host'],
                                    database=self.__config['database'])
            return connection
        except Exception as e:
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
		
