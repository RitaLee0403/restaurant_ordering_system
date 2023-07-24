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
        
    def get_linepay_booking_data(self, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT attractionId, MAX(userId), MAX(date), MAX(time), MAX(price), MAX(name), MAX(email)\
                    FROM booking\
                    INNER JOIN account ON booking.userId = account.id AND userId = %s\
                    GROUP BY attractionId;'
        values = ([f"{id}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    
    def get_pdf_data(self, paymentId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'select payment.id,\
                     payment.userId,\
                     data.name,\
                     payment.date,\
                     payment.time,\
                     account.name,\
                     account.email\
                     from payment\
                    inner join data on \
                    payment.attractionId = data.id &&\
                    payment.id = %s inner join account on payment.userId = account.id;'
        values = ([f"{paymentId}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
        

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
    
    def get_order_attraction_data(self, id):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT data.id, MAX(data.name), MAX(data.address), MIN(picture.pc), MAX(payment.date), MAX(payment.time)\
                    FROM data \
                    JOIN picture ON data.idName = picture.id \
                    JOIN payment on payment.id = %s\
                    where data.id = payment.attractionId GROUP BY data.idName;'
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
        
    def delete_all(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'DELETE FROM `booking` WHERE userId = %s ;'
        values = ([f"{userId}"]) 
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
    
    def get_order_data(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = "SELECT `id`,\
                        `attractionId`,\
                        `time`,\
                        `date`,\
                        `name`,\
                        `email`,\
                        `phone`,\
                        `price` \
                        WHERE `userId` = %s"
        values = ([f"{userId}"]) 
        cursor.execute(execute, values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    

    def upload_headshot(self, userId, headshot):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'INSERT INTO `user_headshot`(`userId`, `headshot`) VALUES(%s, %s)'
        # a = self.convertToBinary(headshot)
        values = (userId, headshot)
        print(headshot)
        cursor.execute(execute,values)
        cnx.commit()
        cursor.close()
        cnx.close()
    
    def get_headshot(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT `headshot` from `user_headshot` WHERE `userId` = %s'
        values = ([f"{userId}"]) 
        cursor.execute(execute,values)
        record = cursor.fetchall()[0][0]
        test = self.convertBinaryToFile(record,"static/images/headshot.png")
        cursor.close()
        cnx.close()
        return test
    
    def get_order_info(self, userId):
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = 'SELECT SUM(DISTINCT price) AS total_price\
                    FROM booking where userId = %s\
                    GROUP BY userId, attractionId;'
        values = ([f"{userId}"]) 
        cursor.execute(execute,values)
        record = cursor.fetchall()
        cursor.close()
        cnx.close()
        return record
    
    def convertToBinary(self,filename):
        with open(filename, 'rb') as file:
            binarydata = file.read()
        return binarydata
    
    def convertBinaryToFile(self,binarydata,filename):
        with open(filename,'wb') as file:
            print("type",type(binarydata))
            file.write(binarydata)
        
        
        