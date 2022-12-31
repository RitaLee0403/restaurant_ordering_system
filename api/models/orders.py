from mysql_connect import pool


class Order:
    def get_history_order(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT payment.id, time, date, payment.name, email, phone, price, data.name as attraction_name, data.address as address, MIN(picture.pc) as picture FROM payment \
                JOIN data ON payment.attractionId = data.id JOIN picture ON data.idName = picture.id WHERE payment.userId = %s\
                GROUP BY payment.id, time, date, payment.name, email, phone, price, data.name, data.address\
                ORDER BY payment.id;'
        values = ([f"{userId}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
