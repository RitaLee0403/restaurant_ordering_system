from flask import Blueprint ,  request
from api.models.attraction import Attraction


attraction_api = Blueprint("attraction_api", __name__)
attractions = Attraction()

@attraction_api.route("/api/attraction/<id>")
def attraction(id):
	id = int(id)
	try:
		if(len(attractions.get_attraction(id)) == 0):
			data = {
				"error":True,
				"message":"景點編號不正確"
			}
			return data,400
		data = {
			"data":attractions.get_attraction(id)
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
		if(len(attractions.show_page(page+1)) == 0):
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
			if(len(attractions.show_page(page+1,keyword)) == 0):
				nextPage = None
				
			data = {
				"nextPage":nextPage,
				"data":attractions.show_page(page,keyword)
			}
			return data,200
		if(keyword == ""):
			data = {
					"nextPage":nextPage,
					"data":attractions.show_page(page)
			}
			return data,200
	except:
			data = {
				"error": True,
				"message":"連線失敗"
			}
			return data,500


     
