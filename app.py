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
@app.route("/attraction/<id>")
def attraction(id):
	try:
		id = int(id)
		if(len(getData.getAttraction(id)) == 0):
			data = {
				"error":True,
				"message":"景點編號不正確"
			}
			return data
		data = {
			"data":getData.getAttraction(id)
		}
		return data
	except:
		data = {
			"error":True,
			"message":"連線失敗"
		}
		return data
		
			
	
	# return render_template("attraction.html")

@app.route("/api/attractions")
def apiAttraction():
	try:
		page = request.args.get("page","0")
		keyword = request.args.get("keyword", "")
		page=int(page)
		if(page < 0 or page > 4):
			data = {
				"error": True,
				"message": "無此頁"
			}
			return data
		if(keyword != ""):
			if(len(getData.showPage(page,keyword)) <= 12 ):
				data = {
					"nextPage":None,
					"data":getData.showPage(page,keyword)
			}
				return data
			else:
				data = {
						"nextPage":page+1,
						"data":getData.showPage(page,keyword)
				}
				return data
		if(keyword == ""):
			data = {
					"nextPage":page+1,
					"data":getData.showPage(page)
			}
			return data
	except:
			data = {
				"error": True,
				"message":"連線失敗"
			}


     
@app.route("/api/categories")
def apiCategories():
    data = {
		"data":getData.getCategories()	
	}
    return data
	
	

@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.run(port=3000,debug=True)