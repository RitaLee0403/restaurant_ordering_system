from mysql_connect import pool

class Login:
    def get_user_data(self, email):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT id,name from `account` WHERE `email` = %s;'
        values = ([f"{email}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    
    def login(self, email, password):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT COUNT(*) from `account` WHERE `email` = %s AND `password` = %s;'
        values = (email, password)
        cursor.execute(execute, values)
        record = cursor.fetchall()
        if(record[0][0] != 0):
            cursor.close()
            cnx.close()
            return True
        cursor.close()
        cnx.close()
        return False