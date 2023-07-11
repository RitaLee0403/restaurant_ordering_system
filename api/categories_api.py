from flask import Blueprint ,  request
from models.categories import Categories
categories_api = Blueprint("categories_api", __name__)
categories = Categories()


@categories_api.route("/api/categories")
def api_categories():
	try:
		data = {
				"data":categories.get_categories()	
			}
		return data,200
	except:
		data = {
				"error": True,
				"data":"連線失敗"	
				}
		return data,500