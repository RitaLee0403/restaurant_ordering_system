from mysql_connect import pool

class Categories:
    def get_categories(self):
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