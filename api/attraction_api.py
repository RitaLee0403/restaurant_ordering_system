from flask import Blueprint ,  request
import mysql_function 


attraction_api = Blueprint("attraction_api", __name__)
getData = mysql_function.ConnectToSql()

@attraction_api.route("/api/attraction/<id>")
def attraction(id):
	id = int(id)
	try:
		if(len(getData.get_attraction(id)) == 0):
			data = {
				"error":True,
				"message":"景點編號不正確"
			}
			return data,400
		data = {
			"data":getData.get_attraction(id)
		}
		return data,200
	except:
		data = {
			"error":True,
			"message":"連線失敗"
		}
		return data,500



@attraction_api.route("/api/attractions/")
def apiAttraction():
	try:
		page = request.args.get("page","0")
		keyword = request.args.get("keyword", "")
		page=int(page)
		if(len(getData.show_page(page+1)) == 0):
			nextPage = None
		else:
			nextPage = page +1

		if(page < 0 or page > 4):
			data = {
				"error": True,
				"message": "無此頁"
			}
			return data,200
		if(keyword != ""):
			if(len(getData.show_page(page+1,keyword)) == 0):
				nextPage = None
				
			data = {
				"nextPage":nextPage,
				"data":getData.show_page(page,keyword)
			}
			return data,200
		if(keyword == ""):
			data = {
					"nextPage":nextPage,
					"data":getData.show_page(page)
			}
			return data,200
	except:
			data = {
				"error": True,
				"message":"連線失敗"
			}
			return data,500


     
