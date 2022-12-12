from flask import Blueprint ,  request
import mysql_function 

categories_api = Blueprint("categories_api", __name__)
getData = mysql_function.ConnectToSql()


@categories_api.route("/api/categories")
def apiCategories():
	try:
		data = {
				"data":getData.getCategories()	
			}
		return data,200
	except:
		data = {
				"error": True,
				"data":"連線失敗"	
				}
		return data,500