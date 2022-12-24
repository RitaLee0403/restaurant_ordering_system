from mysql_connect import pool

class Attraction:
    def get_pc(self,id):
        pcArr = []
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = "SELECT \
                    `picture`.`pc` \
                    from `picture`\
                    INNER JOIN `data` ON `data`.`idName` = `picture`.`id` \
                    AND `data`.`id` = %s;"
        values = ([f"{id}"])
        cursor.execute(execute,values)
        records = cursor.fetchall()
        for k in records:
            pcArr.append(k[0])
        cursor.close()
        cnx.close()
        return pcArr

    def get_attraction(self,id):
        dict = {}
        cnx = pool.get_connection()
        cursor = cnx.cursor()
        execute = "SELECT \
                    `id`,\
                    `name`,\
                    `category`,\
                    `description`,\
                    `address`,\
                    `transport`,\
                    `MRT`,\
                    `latitude`,\
                    `longitude` \
                    FROM \
                    `data` WHERE `data`.`id` = %s;"
        values = ([f"{id}"])
        cursor.execute(execute,values)
        record = cursor.fetchall()
        for k in record:
            images = self.get_pc(id)
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
        cursor.close()
        cnx.close()
        return dict

        
    
    def show_page(self, page, keyword = ""):
        arr = []
        pages = 12 
        firstIndex = 12 * page
        if(keyword == ""):
            
            cnx = pool.get_connection()
            cursor = cnx.cursor()
            execute = "SELECT \
                        Data.`id`,\
                        `name`,\
                        `category`,\
                        `description`,\
                        `address`,\
                        `transport`,\
                        `MRT`,\
                        `latitude`,\
                        `longitude`,\
                        `picture`.`pc` \
                        FROM \
                        (SELECT * FROM `data` LIMIT %s,%s)AS Data \
                        INNER JOIN `picture` ON \
                        (`picture`.`id` = Data.`idName`);"

            values = (firstIndex,pages)
            cursor.execute(execute,values)
            record = cursor.fetchall()
            pcdict = {}
            
            #把圖片放到pcdict
            for i in record:
                if(f"{i[0]}" in pcdict):
                    pcdict[f"{i[0]}"].append(i[9])
                else:
                    pcdict[f"{i[0]}"] = []
                    pcdict[f"{i[0]}"].append(i[9])
            num = - 1
            
            #把資料塞進arr
            for k in record:
                prev = record[num][0]
                
                if(num >= 0):
                    if(prev == k[0]):
                        num +=1
                        continue
        
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
                    "images":pcdict[f"{k[0]}"]
                })
                num +=1
            cursor.close()
            cnx.close() 
        else:
            cnx = pool.get_connection()
            cursor = cnx.cursor()
            execute = "SELECT \
                        Data.`id`,\
                        `name`,\
                        `category`,\
                        `description`,\
                        `address`,\
                        `transport`,\
                        `MRT`,\
                        `latitude`,\
                        `longitude`,\
                        `picture`.`pc` \
                        FROM \
                        (SELECT * FROM `data` WHERE (`name` LIKE %s OR `category` = %s) LIMIT %s,%s)AS Data \
                        INNER JOIN `picture` ON \
                        (`picture`.`id` = Data.`idName`) ;"
            values = (f"%{keyword}%",keyword,firstIndex,pages)
            cursor.execute(execute,values)
            record = cursor.fetchall()
            
            #把圖片放到pcdict
            pcdict = {}
            for i in record:
                if(f"{i[0]}" in pcdict):
                    pcdict[f"{i[0]}"].append(i[9])
                else:
                    pcdict[f"{i[0]}"] = []
                    pcdict[f"{i[0]}"].append(i[9])
            num = - 1

            #把資料塞進arr
            for k in record:
                prev = record[num][0]
                
                if(num >= 0):
                    if(prev == k[0]):
                        num +=1
                        continue
                
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
                    "images":pcdict[f"{k[0]}"]
                })
                num +=1
            cursor.close()
            cnx.close()
        return arr