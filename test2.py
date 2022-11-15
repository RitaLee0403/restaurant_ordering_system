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
def getAttraction(id):
    dict = {}
    cnx = pool.get_connection()
    cursor = cnx.cursor()
    execute = "SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`MRT`,`latitude`,`longitude` FROM `data` WHERE `data`.`id` = %s;"
    values = ([f"{id}"])
    cursor.execute(execute,values)
    record = cursor.fetchall()
    for k in record:
        images = get_pc(0,id)
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
print(getAttraction(5))




    
# def showPage(page):
#     arr = []
#     pages = 12
#     if(page == 4):
#         pages = 10
    
#     index = (12 * page) + 1
#     imageIndex = index
#     for i in range(pages):
#         cnx = pool.get_connection()
#         cursor = cnx.cursor()
#         execute = "SELECT `id`,`name`,`category`,`description`,`address`,`transport`,`MRT`,`latitude`,`longitude` FROM `data` WHERE `idName` = %s"
#         values = ([f"{index}"])
#         cursor.execute(execute,values)
#         record = cursor.fetchall()
#         index +=1
#         for k in record:
#             images = get_pc(imageIndex)
#             arr.append({
#                 "id" : k[0],
#                 "name" : k[1],
#                 "category":k[2],
#                 "description":k[3],
#                 "address":k[4],
#                 "transport":k[5],
#                 "mrt":k[6],
#                 "lat":k[7],
#                 "lng":k[8],
#                 "images":images
#             })
#             imageIndex +=1
            
#         cursor.close()
#         cnx.close()
#     return arr

# showPage(0)
# print(showPage(0))
  

