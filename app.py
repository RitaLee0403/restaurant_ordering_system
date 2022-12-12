from flask import Flask, render_template, redirect, request, make_response
from api import api_blueprint
import jwt
import mysql_function 
import datetime
import time

app=Flask(__name__)
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
jwt_key = "dsjlfjkdlasjfklsdafjaksldfjkaksdlfjaslfksaldfjalsfj"
getData = mysql_function.ConnectToSql()


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





@app.route("/api/booking", methods = ["POST"])
def apiBookingPost():
	try:
		getId = request.cookies.get("token")
		if(getId and (initCookie == getId)):
			print(1)
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			bookingData = request.json
			orderDate = bookingData["date"]
			orderYear = int(orderDate[0:4])
			orderMonth = int(orderDate[5:7])
			orderDay = int(orderDate[8:])
			localtime = time.localtime()
			year = int(time.strftime("%Y", localtime))
			month = int(time.strftime("%m", localtime))
			day = int(time.strftime("%d", localtime))
			print(2)
			if(orderYear < year):  #判斷是否預約到過去的日期
				return {"error":True, "message" : "日期輸入錯誤"},400
			elif(orderYear == year and orderMonth < month):
				return {"error":True, "message" : "日期輸入錯誤"},400
			elif(orderYear == year and orderMonth == month and orderDay < day):
				return {"error":True, "message" : "日期輸入錯誤"},400
			print(3)
			print(bookingData)
			getData.booking(getId,bookingData)
			print(4)
			return {"ok" : True},200
		else:
			return {"error":True, "message" : "尚未登入"},403
	except:
		return {"error":True, "message":'伺服器內部錯誤'},500
	
	


@app.route("/api/booking", methods = ["GET","DELETE"])
def apiBooking():
	if request.method == "GET":
		getId = request.cookies.get("token")
		if(getId and (initCookie == getId)): 
		
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			datas = getData.getBookingData(getId)
			bookingDatas = {"data":[]
			}
			attraction = {"attraction":{}}
			prev = -1
			for data in datas:
				if(data[0] == prev):
					continue
				prev = data[0]
				attraction["attraction"]["id"] = data[0]
				attraction["attraction"]["name"] = data[1]
				attraction["attraction"]["address"] = data[2]
				attraction["attraction"]["image"] = data[3]
				attraction["date"] = data [4]
				attraction["time"] = data[5]
				attraction["price"] = data[6]
				bookingDatas["data"].append(attraction)
				attraction = {"attraction":{}}

			return bookingDatas 
		else:
			return {"error":True,"message" : "未登入系統，拒絕存取"},403
	if request.method == "DELETE":
		try:
			deleteData = request.json
			deleteData = deleteData["attractionId"]
			getId = request.cookies.get("token")
			getId = jwt.decode(getId, jwt_key, algorithms="HS256")
			getId = getId["data"]["id"]
			getData.deleteBooking(getId, deleteData)
			return {"ok":True},200
		except:
			return {"error":True , "message" : "刪除失敗"},403


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
					expire_date = datetime.datetime.now()
					expire_date = expire_date + datetime.timedelta(days=7)
					response.set_cookie("token", token,expires= expire_date)
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
	cookie = request.cookies.get("token")
	if(cookie and (initCookie == cookie)):
		return render_template("booking.html")	
	return redirect("/")   
    
        



@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")

app.register_blueprint(api_blueprint)

app.run(host = "0.0.0.0",port=3000,debug=True)