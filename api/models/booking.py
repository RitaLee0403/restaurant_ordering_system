from mysql_connect import pool


class Booking:    
    def add_data_to_booking(self, id, data):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'INSERT INTO `booking`(userId, attractionId, date, time, price) VALUES(%s,%s,%s,%s,%s);'
        attractionId = data["attractionId"]
        date = data["date"]
        time = data["time"]
        price = data["price"]
        values = (id,attractionId, date, time, price)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
        
    def get_booking_data(self, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT data.id, MAX(data.name), MAX(data.address), MIN(picture.pc), MAX(booking.date), MAX(booking.time), MAX(booking.price) \
                    FROM data \
                    JOIN picture ON data.idName = picture.id \
                    JOIN ( \
                    SELECT userId,attractionId, date, time, price \
                    FROM booking \
                    WHERE booking.userId = %s\
                    ) booking ON data.id = booking.attractionId GROUP BY data.idName;'

        values = ([f"{id}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    
    def delete_booking(self, userId, attractionId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'DELETE FROM `booking` WHERE userId = %s AND attractionId = %s;'
        values = (userId, attractionId)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
    
    def order(self, id, userId, attractionId, time, date, name, email, phone, price  ):
        cnx = pool.get_connection()
        cursor = cnx.cursor() 
        execute = 'INSERT INTO `payment`(\
                id,\
                userId,\
                attractionId,\
                time,\
                date,\
                name,\
                email,\
                phone,\
                price)\
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s);'
        values = (id, userId, attractionId, time, date, name, email, phone, price)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
        
        
    def get_order_data(self, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'Select \
                `id`,\
                `name`,\
                email,\
                phone,\
                price\
         from payment where id = %s limit 1'
        values = ([f"{id}"]) 
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
        
    
    # def get_order_number(userId):
    #     cnx = pool.get_connection()
    #     cursor = cnx.cursor() 
    #     execute = 'SELECT id from `order_product` where userId = %s'
    #     values = ([f'{userId}'])
    #     cursor.execute(execute,values)
        
    #     record = cursor.fetchall()
    #     cursor.close()
    #     cnx.close()
    #     return record
        
        
        