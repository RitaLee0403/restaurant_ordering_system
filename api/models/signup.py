from mysql_connect import pool

class Signup:
    def is_signup_success(self,email):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT `email` from `account` WHERE `email` = %s'
        values = ([f"{email}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        if(len(record) == 0):
            cursor.close()
            cnx.close()
            return True
        cursor.close()
        cnx.close()
        return False
    
    def signup(self,name, email, password):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'INSERT INTO `account`(name, email, password) VALUES(%s, %s, %s);'
        values = (name,email,password)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()