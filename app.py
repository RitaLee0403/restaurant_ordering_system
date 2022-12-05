from flask import Flask, render_template, jsonify, request, make_response
from view.api import api_blueprint
import jwt
from view.api_fun import *


app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
jwt_key = "dsjlfjkdlasjfklsdafjaksldfjkaksdlfjaslfksaldfjalsfj"
getData = ConnectToSql()
payload_data = None

# Pages
@app.route("/")
def index():	
	return render_template("index.html")

@app.route("/attraction/<id>")
def showAttraction(id):
	return render_template("attraction.html")

@app.route("/api/user", methods = ["POST"])
def user():
	try:
		ok = {
			"ok" : True
		}
		data = request.json
		if(getData.checkSignup(data["email"])):
			getData.addUserData(data["name"], data["email"], data["password"])
			return ok,200
		else:
			
			return {
				"error" : True,
				"message": "此email已經註冊過了"
			},400

	except:
		return {
			"error" : True,
			"message" : "伺服器出現錯誤"
		}
 
    
@app.route("/api/user/auth" , methods = ["GET", "PUT", "DELETE"])
def userAuth():
		ok = {
			"ok" : True
		}
		try:
			if request.method == 'PUT':
				data = request.json
				if(getData.login(data["email"], data["password"])):
					userData = getData.getUserData(data["email"])
					response = make_response(ok)
					global payload_data
					payload_data = {
						"data" : {
						"id" : userData[0][0],
						"name" : userData[0][1],
						"email" : data["email"]
						}
					}
					token = jwt.encode(payload_data, jwt_key, algorithm="HS256")
					response.set_cookie("token", token)
					global initCookie
					initCookie = token
					return response, 200
				else:
					error = {
						"error" : True,
						"message" : "帳號或密碼錯誤"
					}
					return error,400
			if request.method == 'GET':
				cookie = request.cookies.get("token")
				#cookie 被改過的話要退出
				if(cookie and (initCookie == cookie)): 
					cookie = jwt.decode(cookie, jwt_key, algorithms="HS256")
					return cookie,200
				else:
					noneError = {
						"data" : None
					}
					
					return noneError,200
			if request.method == "DELETE":
				response = make_response(ok)
				response.delete_cookie("token")
				return response,200
		except:
			error = {
				"error" : True,
				"message" : "伺服器出現錯誤"
			}
			return error, 500
    
    
    
    
    
        





@app.route("/booking")
def booking():
	return render_template("booking.html")

@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.register_blueprint(api_blueprint)

app.run(host = "0.0.0.0",port=3000,debug=True)