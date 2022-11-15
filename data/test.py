import json
from mysql.connector import pooling


pool = pooling.MySQLConnectionPool(
        pool_name = "my_pool",
        pool_size = 2,
        pool_reset_session=True,
        host = '127.0.0.1',
        database = 'taipei_attraction',
        user = 'root',
        password = "0403",
        charset='utf8'
    )


# test = ["a","b"]
# if("c" in test):
#     print(1)
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
print(arr)

# path ='C:/Users/rita0/OneDrive/桌面/taipei-day-trip/data/taipei-attractions.json'
# with open (path,  'r', encoding = 'utf-8') as file:
#     file = file.read()
#     file = json.loads(file)
#     file = file["result"]["results"]

# # count = file[3]["file"].count("https")
# # file = file[1]["file"]
# # print(file)
# # test = "asdfa"
# # origin = 0
# data = file

# for i in range(58):
#     pc_array = []   
#     count = file[i]["file"].count("https")
#     origin = 0
#     data = file[i]["file"]
#     for k in range(count):
        
        
#         cnx = pool.get_connection()
#         cursor = cnx.cursor()
#         index = data.find("https",origin)
#         answer = data.find("https",index + 1)
#         origin = data.find("https",answer)

#         if(".mp" in data[index:answer] or  ".fl" in data[index:answer]):#過濾mp3,flv檔案
#             cursor.close()
#             cnx.close()
#             continue
#         if(k == count-1):
#             pc_array.append(data[index:])
#             print(data[index:])
            
#             execute = "INSERT INTO `picture`(`id`,`pc`) VALUES(%s,%s);"
#             values = (i+1,data[index:])
#             cursor.execute(execute,values) 
#             cnx.commit()
#             cursor.close()
#             cnx.close()
#             break
#         pc_array.append(data[index:answer])
#         print(data[index:answer])
#         execute = "INSERT INTO `picture`(`id`,`pc`) VALUES(%s,%s);"
#         values = (i+1,data[index:answer])
#         cursor.execute(execute,values) 
#         cnx.commit()
#         cursor.close()
#         cnx.close()

    
    # for i in pc_array:
    #     print(i)



# for i in range(58):  
    
#     print(file[i])
                


    
    