from mysql.connector import pooling
from dotenv import load_dotenv
import os
load_dotenv()


mysqlPassword = os.getenv("password")
mysqlHost = os.getenv("mysqlHost")

pool = pooling.MySQLConnectionPool(
        pool_name = "my_pool",
        pool_size = 30,
        pool_reset_session=True,
        host = mysqlHost,
        database = 'taipei_attraction',
        user = 'admin',
        password = mysqlPassword,
        charset='utf8',
        auth_plugin='mysql_native_password'

    )

  
        
    
        
    
    
        
        
    
