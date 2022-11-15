import json
from mysql.connector import pooling


pool = pooling.MySQLConnectionPool(
        pool_name = "my_pool",
        pool_size = 10,
        pool_reset_session=True,
        host = '127.0.0.1',
        database = 'taipei_attraction',
        user = 'root',
        password = "0403",
        charset='utf8'
    )

class ConnectToSql:
    def getCategories(self):
        arr = []
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        cursor.execute("SELECT `data`.`category` from `data`;")
        records = cursor.fetchall()
        for i in records:
            if(i[0] in arr):
                continue
            arr.append(i[0])
        cursor.close()
        cnx.close()
        return arr
        
    def get_pc(self, index, id = None):
        pcArr = []
        if(id == None):
            for i in range(1):
                cnx = pool.get_connection()
                cursor = cnx.cursor()
                execute = "SELECT `picture`.`pc` from `picture` INNER JOIN `data` ON `data`.`idName` = `picture`.`id` AND `data`.`idName` = %s;"
                values = ([f"{index}"])
                cursor.execute(execute,values)
                records = cursor.fetchall()
                for k in records:
                    pcArr.append(k[0])
                index+=1
                cursor.close()
                cnx.close()
            return pcArr
        else:
            cnx = pool.get_connection()
            cursor = cnx.cursor()
            execute = "SELECT `picture`.`pc` from `picture` INNER JOIN `data` ON `data`.`idName` = `picture`.`id` AND `data`.`id` = %s;"
            values = ([f"{id}"])
            cursor.execute(execute,values)
            records = cursor.fetchall()
            for k in records:
                pcArr.append(k[0])
            cursor.close()
            cnx.close()
            return pcArr

    def getAttraction(self,id):
        dict = {}
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = "SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`MRT`,`latitude`,`longitude` FROM `data` WHERE `data`.`id` = %s;"
        values = ([f"{id}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        for k in record:
            images = self.get_pc(0,id)
            dict ={
                "id" : k[0],
                "name" : k[1],
                "category":k[2],
                "description":k[3],
                "address":k[4],
                "transport":k[5],
                "mrt":k[6],
                "lat":k[7],
                "lng":k[8],
                "images":images
            }
        return dict

        
    
    def showPage(self, page, keyword = None):
        arr = []
        pages = 12
        if(page == 4):
            pages = 10
        
        index = (12 * page) + 1
        imageIndex = index
        if(keyword == None):
            for i in range(pages):
                cnx = pool.get_connection()
                cursor = cnx.cursor()
                execute = "SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`MRT`,`latitude`,`longitude` FROM `data` WHERE `idName` = %s;"
                values = ([f"{index}"])
                cursor.execute(execute,values)
                record = cursor.fetchall()
                index +=1
                for k in record:
                    images = self.get_pc(imageIndex)
                    arr.append({
                        "id" : k[0],
                        "name" : k[1],
                        "category":k[2],
                        "description":k[3],
                        "address":k[4],
                        "transport":k[5],
                        "mrt":k[6],
                        "lat":k[7],
                        "lng":k[8],
                        "images":images
                    })
                    imageIndex +=1
                    
                cursor.close()
                cnx.close()
        else:
            cnx = pool.get_connection()
            cursor = cnx.cursor()
            execute = "SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`MRT`,`latitude`,`longitude` FROM `data` WHERE `data`.`name` LIKE %s"
            values = ([f"%{keyword}%"])
            cursor.execute(execute,values)
            record = cursor.fetchall()
            index +=1
            size = len(record)
            if(size > 12):
                size = 12
            count = 1
            for k in record:
                if(count > 12):
                    break
                images = self.get_pc(imageIndex)
                arr.append({
                    "id" : k[0],
                    "name" : k[1],
                    "category":k[2],
                    "description":k[3],
                    "address":k[4],
                    "transport":k[5],
                    "mrt":k[6],
                    "lat":k[7],
                    "lng":k[8],
                    "images":images
                })
                imageIndex += 1
                count += 1
            cursor.close()
            cnx.close()
            
        return arr
