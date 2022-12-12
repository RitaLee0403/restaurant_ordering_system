from flask import Blueprint ,  request
import mysql_function 

categories_api = Blueprint("categories_api", __name__)
getData = mysql_function.ConnectToSql()


@categories_api.route("/api/categories")
def api_categories():
	try:
		data = {
				"data":getData.get_categories()	
			}
		return data,200
	except:
		data = {
				"error": True,
				"data":"連線失敗"	
				}
		return data,500