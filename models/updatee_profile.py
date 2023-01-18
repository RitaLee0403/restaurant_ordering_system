from mysql_connect import pool

class   UpdateProfile:
    def update_name(self, name, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'UPDATE `account` SET `name` = %s  WHERE `id` = %s ;'
        values = (name, id)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
    
    def update_email(self, email, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'UPDATE `account` SET `email` = %s  WHERE `id` = %s ;'
        values = (email, id)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
        
    def get_user_data(self, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT `name`,`email` from `account` WHERE `id` = %s ;'
        values = ([f"{id}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    
    def is_email_already_in_use(self, email, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT COUNT(*) from `account` WHERE `email` = %s AND `id` <> %s;'
        values = (email, id)
        cursor.execute(execute, values)
        record = cursor.fetchall()
        if(record[0][0] == 0):
            cursor.close()
            cnx.close()
            return False
        cursor.close()
        cnx.close()
        return True