from mysql_connect import pool


class Order:
    def get_history_order(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'select MAX(payment.id),MAX(time),MAX(date),MAX(payment.name),MAX(email),MAX(phone),MAX(price),MAX(data.name),MAX(data.address),MIN(picture.pc) from payment\
                join data on payment.attractionId = data.id\
                join picture on data.idName = picture.id\
                where payment.userId = %s GROUP BY data.idName order by `payment`.`id`;'
        values = ([f"{userId}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
