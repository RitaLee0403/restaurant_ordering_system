from flask import *
from api_fun import *
app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
getData = ConnectToSql()
# Pages
@app.route("/")
def index():
	return render_template("index.html")

@app.route("/api/attraction/<id>")
def attraction(id):
	id = int(id)
	try:
		if(len(getData.getAttraction(id)) == 0):
			data = {
				"error":True,
				"message":"景點編號不正確"
			}
			return data,400
		data = {
			"data":getData.getAttraction(id)
		}
		return data,200
	except:
		data = {
			"error":True,
			"message":"連線失敗"
		}
		return data,500

@app.route("/api/attractions/")
def apiAttraction():
	try:
		page = request.args.get("page","0")
		keyword = request.args.get("keyword", "")
		page=int(page)
		if(len(getData.showPage(page+1)) == 0):
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
			if(len(getData.showPage(page+1,keyword)) == 0):
				nextPage = None
				
			data = {
				"nextPage":nextPage,
				"data":getData.showPage(page,keyword)
			}
			return data,200
		if(keyword == ""):
			data = {
					"nextPage":nextPage,
					"data":getData.showPage(page)
			}
			return data,200
	except:
			data = {
				"error": True,
				"message":"連線失敗"
			}
			return data,500


     
@app.route("/api/categories")
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
		
	

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run( port=3000,debug=True)#host = "0.0.0.0"