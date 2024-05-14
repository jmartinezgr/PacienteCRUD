import pymysql

class Connection:
    _DATABASE = 'CRUDINFO'
    _USERNAME = 'root'
    _PASSWORD = ''
    _DB_PORT = 3306
    _HOST = 'localhost'
    _connection = None

    @classmethod
    def get_connection(cls):
        if cls._connection is None:
            try:
                cls._connection = pymysql.connect(
                    host=cls._HOST,
                    user=cls._USERNAME,
                    password=cls._PASSWORD,
                    port=cls._DB_PORT,
                    database=cls._DATABASE
                )
                return cls._connection
            except Exception as e:
                print(f"An error occurred while obtaining the database connection: {e}")
        else:
            return cls._connection
        
    @classmethod
    def get_cursor(cls):
        connection = cls.get_connection()
        return connection.cursor()

if __name__ == "__main__":
    Connection.get_connection()
    Connection.get_cursor()
